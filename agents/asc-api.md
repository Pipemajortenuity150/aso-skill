# App Store Connect API Agent

Direct API access to App Store Connect without external dependencies.

## Authentication Methods

### 1. API Key Authentication (Recommended)
Requires:
- Issuer ID
- Key ID
- Private Key (.p8 file)

```bash
# Check for existing credentials
cat ~/.aso/credentials.json 2>/dev/null || echo "No credentials"
```

### 2. JWT Token Generation

```python
import jwt
import time
import json
import os

def generate_asc_token():
    """Generate JWT token for App Store Connect API."""
    creds_path = os.path.expanduser("~/.aso/credentials.json")

    if not os.path.exists(creds_path):
        raise Exception("No credentials found. Run /aso-setup first.")

    with open(creds_path) as f:
        creds = json.load(f)

    # Read private key
    with open(os.path.expanduser(creds["privateKeyPath"])) as f:
        private_key = f.read()

    # Generate JWT
    now = int(time.time())
    payload = {
        "iss": creds["issuerId"],
        "iat": now,
        "exp": now + 1200,  # 20 minutes
        "aud": "appstoreconnect-v1"
    }

    headers = {
        "alg": "ES256",
        "kid": creds["keyId"],
        "typ": "JWT"
    }

    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    return token

# Usage
token = generate_asc_token()
print(f"Bearer {token}")
```

### 3. API Request Helper

```python
import urllib.request
import json

def asc_request(method, endpoint, data=None, token=None):
    """Make authenticated request to ASC API."""
    base_url = "https://api.appstoreconnect.apple.com/v1"
    url = f"{base_url}/{endpoint}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = json.dumps(data).encode() if data else None

    req = urllib.request.Request(url, data=body, method=method, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error = e.read().decode()
        raise Exception(f"HTTP {e.code}: {error[:500]}")
```

---

## Core API Operations

### List Apps
```python
token = generate_asc_token()
apps = asc_request("GET", "apps?limit=200", token=token)
for app in apps["data"]:
    print(f'{app["id"]}: {app["attributes"]["name"]}')
```

### Get App Details
```python
app = asc_request("GET", f"apps/{APP_ID}", token=token)
print(json.dumps(app, indent=2))
```

### List App Store Versions
```python
versions = asc_request("GET", f"apps/{APP_ID}/appStoreVersions", token=token)
for v in versions["data"]:
    print(f'{v["id"]}: {v["attributes"]["versionString"]} - {v["attributes"]["appStoreState"]}')
```

---

## Metadata Operations

### Get Localizations
```python
localizations = asc_request("GET", f"appStoreVersions/{VERSION_ID}/appStoreVersionLocalizations", token=token)
for loc in localizations["data"]:
    attrs = loc["attributes"]
    print(f'{loc["id"]}: {attrs["locale"]}')
    print(f'  Description: {len(attrs.get("description", ""))} chars')
    print(f'  Keywords: {attrs.get("keywords", "N/A")}')
```

### Update Localization
```python
data = {
    "data": {
        "type": "appStoreVersionLocalizations",
        "id": LOCALIZATION_ID,
        "attributes": {
            "description": "New description...",
            "keywords": "keyword1,keyword2,keyword3",
            "promotionalText": "Promo text...",
            "marketingUrl": "https://...",
            "supportUrl": "https://..."
        }
    }
}
asc_request("PATCH", f"appStoreVersionLocalizations/{LOCALIZATION_ID}", data=data, token=token)
```

### Create New Locale
```python
data = {
    "data": {
        "type": "appStoreVersionLocalizations",
        "attributes": {
            "locale": "tr",
            "description": "Turkish description...",
            "keywords": "anahtar,kelime",
            "promotionalText": "Tanıtım metni..."
        },
        "relationships": {
            "appStoreVersion": {
                "data": {"type": "appStoreVersions", "id": VERSION_ID}
            }
        }
    }
}
asc_request("POST", "appStoreVersionLocalizations", data=data, token=token)
```

---

## App Info (Title/Subtitle)

### Get App Info Localizations
```python
# First get app info ID
app_infos = asc_request("GET", f"apps/{APP_ID}/appInfos", token=token)
app_info_id = app_infos["data"][0]["id"]

# Get localizations
locs = asc_request("GET", f"appInfos/{app_info_id}/appInfoLocalizations", token=token)
for loc in locs["data"]:
    attrs = loc["attributes"]
    print(f'{attrs["locale"]}: {attrs.get("name")} - {attrs.get("subtitle")}')
```

### Update App Info (Title/Subtitle)
```python
data = {
    "data": {
        "type": "appInfoLocalizations",
        "id": APP_INFO_LOC_ID,
        "attributes": {
            "name": "New App Title",
            "subtitle": "New Subtitle",
            "privacyPolicyUrl": "https://..."
        }
    }
}
asc_request("PATCH", f"appInfoLocalizations/{APP_INFO_LOC_ID}", data=data, token=token)
```

---

## In-App Purchases

### List IAPs
```python
iaps = asc_request("GET", f"apps/{APP_ID}/inAppPurchasesV2", token=token)
for iap in iaps["data"]:
    attrs = iap["attributes"]
    print(f'{iap["id"]}: {attrs["productId"]} - {attrs["name"]} ({attrs["state"]})')
```

### List Subscriptions
```python
groups = asc_request("GET", f"apps/{APP_ID}/subscriptionGroups?include=subscriptions", token=token)
for sub in groups.get("included", []):
    if sub["type"] == "subscriptions":
        attrs = sub["attributes"]
        print(f'{sub["id"]}: {attrs["productId"]} - {attrs["name"]} ({attrs["state"]})')
```

---

## iris API (Web Session)

For operations not supported by public API (like privacy labels), use iris API with web session:

### Session File Format
`~/.aso/web-session.json`:
```json
{
  "cookies": "myacinfo=...; dqsid=...; ...",
  "expires": "2026-04-05T12:00:00Z"
}
```

### iris API Request
```python
import json
import os
import urllib.request

def iris_request(method, endpoint, data=None):
    """Make request to iris API using web session."""
    session_path = os.path.expanduser("~/.aso/web-session.json")

    if not os.path.exists(session_path):
        raise Exception("No web session. Login to App Store Connect in browser and export cookies.")

    with open(session_path) as f:
        session = json.load(f)

    url = f"https://appstoreconnect.apple.com/iris/v1/{endpoint}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://appstoreconnect.apple.com",
        "Referer": "https://appstoreconnect.apple.com/",
        "Cookie": session["cookies"]
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise Exception("Session expired. Re-login to App Store Connect.")
        raise Exception(f"HTTP {e.code}: {e.read().decode()[:500]}")
```

---

## Dependencies

Required Python packages:
```bash
pip3 install PyJWT cryptography
```

Or use jwt-less approach with pre-generated tokens.

---

## Credential Storage

`~/.aso/credentials.json`:
```json
{
  "issuerId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "keyId": "XXXXXXXXXX",
  "privateKeyPath": "~/.aso/AuthKey_XXXXXXXXXX.p8"
}
```

`~/.aso/web-session.json` (for iris API):
```json
{
  "cookies": "cookie_string_here",
  "expires": "ISO_DATE"
}
```
