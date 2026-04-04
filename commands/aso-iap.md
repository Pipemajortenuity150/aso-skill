# /aso-iap Command

Set up In-App Purchases and Subscriptions for App Store Connect.

## Trigger
- `/aso-iap` or `/aso-iap AppName`
- "set up IAPs", "configure subscriptions", "add in-app purchases"

## Prerequisites
- API Key or Web Session configured (`~/.aso/`)
- App created in App Store Connect

## Workflow

### 1. Check Authentication

```python
import os

api_key = os.path.exists(os.path.expanduser("~/.aso/credentials.json"))
web_session = os.path.exists(os.path.expanduser("~/.aso/web-session.json"))

if api_key:
    print("✅ API Key configured")
if web_session:
    print("✅ Web session configured")
if not api_key and not web_session:
    print("❌ No credentials - run /aso-setup")
```

### 2. Generate API Token

```python
import jwt, time, json, os

def generate_token():
    with open(os.path.expanduser("~/.aso/credentials.json")) as f:
        creds = json.load(f)
    with open(os.path.expanduser(creds["privateKeyPath"])) as f:
        pk = f.read()
    return jwt.encode(
        {"iss": creds["issuerId"], "iat": int(time.time()), "exp": int(time.time())+1200, "aud": "appstoreconnect-v1"},
        pk, algorithm="ES256", headers={"kid": creds["keyId"], "typ": "JWT"}
    )
```

### 3. List Current IAPs & Subscriptions

**Using Public API:**
```python
import urllib.request, json

def api(method, endpoint, token, data=None):
    url = f"https://api.appstoreconnect.apple.com/v1/{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

token = generate_token()

# List IAPs
iaps = api("GET", f"apps/{APP_ID}/inAppPurchasesV2", token)
print("In-App Purchases:")
for iap in iaps["data"]:
    attrs = iap["attributes"]
    print(f'  {attrs["productId"]}: {attrs["name"]} ({attrs["state"]})')

# List Subscriptions
groups = api("GET", f"apps/{APP_ID}/subscriptionGroups?include=subscriptions", token)
print("\nSubscriptions:")
for sub in groups.get("included", []):
    if sub["type"] == "subscriptions":
        attrs = sub["attributes"]
        print(f'  {attrs["productId"]}: {attrs["name"]} ({attrs["state"]})')
```

### 4. Ask User What To Do

Options:
1. **Create new IAP** → Guide through creation
2. **Create new Subscription** → Guide through subscription group + product
3. **Attach existing to version** → Use attach workflow
4. **List all** → Show current state

### 5. Create New IAP

```python
def create_iap(app_id, product_id, name, iap_type, token):
    """
    iap_type: CONSUMABLE, NON_CONSUMABLE, NON_RENEWING_SUBSCRIPTION
    """
    data = {
        "data": {
            "type": "inAppPurchases",
            "attributes": {
                "productId": product_id,
                "name": name,
                "inAppPurchaseType": iap_type,
                "reviewNote": "Description for App Review"
            },
            "relationships": {
                "app": {"data": {"type": "apps", "id": app_id}}
            }
        }
    }
    return api("POST", "inAppPurchasesV2", token, data)

# Example: Create credit pack
iap = create_iap(APP_ID, "com.myapp.credits.50", "50 Credits", "CONSUMABLE", token)
print(f"Created IAP: {iap['data']['id']}")
```

### 6. Attach to Version (via iris API)

For items in `READY_TO_SUBMIT` state, use iris API with web session:

```python
import json, urllib.request, os

def iris_request(method, endpoint, data=None):
    with open(os.path.expanduser("~/.aso/web-session.json")) as f:
        session = json.load(f)

    url = f"https://appstoreconnect.apple.com/iris/v1/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Cookie": session["cookies"],
        "X-Requested-With": "XMLHttpRequest"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# Attach Subscription
def attach_subscription(sub_id):
    data = {
        "data": {
            "type": "subscriptionSubmissions",
            "attributes": {"submitWithNextAppStoreVersion": True},
            "relationships": {
                "subscription": {"data": {"type": "subscriptions", "id": sub_id}}
            }
        }
    }
    return iris_request("POST", "subscriptionSubmissions", data)

# Attach IAP
def attach_iap(iap_id):
    data = {
        "data": {
            "type": "inAppPurchaseSubmissions",
            "attributes": {"submitWithNextAppStoreVersion": True},
            "relationships": {
                "inAppPurchaseV2": {"data": {"type": "inAppPurchases", "id": iap_id}}
            }
        }
    }
    return iris_request("POST", "inAppPurchaseSubmissions", data)
```

### 7. Verify

After attachment, run `/aso-status` to verify submission readiness.

## Common IAP Patterns

### Credit Packs (Consumable)
```
- 5 Credits: $0.99 (com.app.credits.5)
- 15 Credits: $1.99 (com.app.credits.15)
- 50 Credits: $4.99 (com.app.credits.50)
```

### Subscription Tiers
```
- Monthly Pro: $4.99/month
- Yearly Pro: $39.99/year (save 33%)
- Lifetime: $99.99 one-time (NON_CONSUMABLE)
```

## Error Handling

### 409 "Already set to submit"
Item is already attached. This is OK - treat as success.

### 401 Not Authorized
API key expired or web session expired. Re-run `/aso-setup`.

### "FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION"
Use iris API (not public API) - it supports `submitWithNextAppStoreVersion`.

## Agent Notes

- Always list IAPs/subs first to show current state
- Confirm with user before attaching
- Use iris API for attach (not public ASC API)
- Never print credentials or session cookies
- Rate limit: 350ms between requests
