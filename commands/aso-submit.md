# /aso-submit Command

Submit app to App Store Connect with metadata, privacy labels, and screenshots.

## Trigger
- `/aso-submit` or `/aso-submit AppName`
- "submit to app store", "push metadata", "deploy to ASC"

## Prerequisites
- API Key configured (`~/.aso/credentials.json`)
- App created in App Store Connect
- Build uploaded and attached to version
- Metadata generated (via `/aso` or `/aso-audit`)

## Workflow

### 1. Check Authentication

```python
import os, json

creds_path = os.path.expanduser("~/.aso/credentials.json")
if os.path.exists(creds_path):
    with open(creds_path) as f:
        creds = json.load(f)
    print(f"✅ API Key configured (Key ID: {creds['keyId']})")
else:
    print("❌ No credentials - run /aso-setup")
```

### 2. Generate JWT Token

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

### 3. Get App Info

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
apps = api("GET", "apps", token)
for app in apps["data"]:
    print(f'{app["id"]}: {app["attributes"]["name"]}')
```

### 4. Privacy Labels (via iris API)

Privacy labels require web session authentication (cookies):

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

# Get current privacy
privacy = iris_request("GET", f"apps/{APP_ID}/appPrivacy")

# Apply privacy config
privacy_data = {
    "data": {
        "type": "appPrivacies",
        "id": privacy["data"]["id"],
        "attributes": {
            "dataUsages": [
                {"category": "CRASH_DATA", "purposes": ["ANALYTICS"], "dataProtections": ["DATA_NOT_LINKED_TO_YOU"]}
            ]
        }
    }
}
iris_request("PATCH", f"appPrivacies/{privacy['data']['id']}", privacy_data)
```

### 5. Metadata Push (Multi-Language)

**Get version ID:**
```python
versions = api("GET", f"apps/{APP_ID}/appStoreVersions?filter[appStoreState]=PREPARE_FOR_SUBMISSION", token)
version_id = versions["data"][0]["id"]
```

**Get localizations:**
```python
locs = api("GET", f"appStoreVersions/{version_id}/appStoreVersionLocalizations", token)
for loc in locs["data"]:
    print(f'{loc["id"]}: {loc["attributes"]["locale"]}')
```

**Update version localization (description, keywords):**
```python
loc_id = "YOUR_LOCALIZATION_ID"
data = {
    "data": {
        "type": "appStoreVersionLocalizations",
        "id": loc_id,
        "attributes": {
            "description": "Your full description here...",
            "keywords": "keyword1,keyword2,keyword3",
            "promotionalText": "Promo text here...",
            "supportUrl": "https://yourapp.com/support",
            "marketingUrl": "https://yourapp.com"
        }
    }
}
api("PATCH", f"appStoreVersionLocalizations/{loc_id}", token, data)
```

**Update app info (title, subtitle):**
```python
# Get app info ID
app_infos = api("GET", f"apps/{APP_ID}/appInfos", token)
app_info_id = app_infos["data"][0]["id"]

# Get app info localizations
app_info_locs = api("GET", f"appInfos/{app_info_id}/appInfoLocalizations", token)

# Update title and subtitle
for loc in app_info_locs["data"]:
    data = {
        "data": {
            "type": "appInfoLocalizations",
            "id": loc["id"],
            "attributes": {
                "name": "Your App Title",
                "subtitle": "Your App Subtitle",
                "privacyPolicyUrl": "https://yourapp.com/privacy"
            }
        }
    }
    api("PATCH", f"appInfoLocalizations/{loc['id']}", token, data)
```

### 6. Screenshots Upload

```python
# Get screenshot sets
ss_sets = api("GET", f"appStoreVersionLocalizations/{loc_id}/appScreenshotSets", token)

# Create screenshot set if needed
if not ss_sets["data"]:
    data = {
        "data": {
            "type": "appScreenshotSets",
            "attributes": {
                "screenshotDisplayType": "APP_IPHONE_67"  # or APP_IPHONE_65, APP_IPAD_PRO_129, etc.
            },
            "relationships": {
                "appStoreVersionLocalization": {
                    "data": {"type": "appStoreVersionLocalizations", "id": loc_id}
                }
            }
        }
    }
    ss_set = api("POST", "appScreenshotSets", token, data)
    ss_set_id = ss_set["data"]["id"]
```

### 7. IAP Attachment (If Applicable)

See `/aso-iap` command for attaching IAPs and subscriptions.

### 8. Verify Submission Readiness

Run `/aso-status` to check all required items.

## Quick Checklist

Before `/aso-submit`:
- [ ] Build uploaded
- [ ] App icon (1024x1024) in build
- [ ] Screenshots ready
- [ ] Metadata generated
- [ ] Privacy policy URL live
- [ ] Support URL live

During `/aso-submit`:
- [ ] Privacy labels applied (via iris API)
- [ ] Metadata pushed (all languages)
- [ ] Screenshots uploaded
- [ ] IAPs attached (if any)

After:
- [ ] Run `/aso-status` to verify
- [ ] Submit for review via ASC web UI

## Locale Mapping

| Our Format | ASC Locale |
|------------|------------|
| en | en-GB |
| tr | tr |
| de | de-DE |
| fr | fr-FR |
| es | es-ES |
| it | it |
| pt-BR | pt-BR |
| ja | ja |
| ko | ko |
| zh-Hans | zh-Hans |

## Error Handling

### 401 Unauthorized
API key invalid or expired. Check credentials at `~/.aso/credentials.json`.

### Metadata validation failed
Check character limits and duplicate keywords.

### Screenshot upload failed
Verify dimensions and file format (PNG/JPEG).

## Agent Notes

- Always preview before applying
- Support any number of languages
- Confirm each step with user
- Never print API tokens or credentials
