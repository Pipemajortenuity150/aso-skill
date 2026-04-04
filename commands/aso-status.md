# /aso-status Command

Check App Store Connect submission readiness.

## Trigger
- `/aso-status` or `/aso-status AppName`
- "check submission", "what's missing", "am I ready to submit"

## Output Example

```
📱 Submission Readiness - MyApp

App Identity
────────────────────────────────────────
  App Name:         MyApp - Smart Photo Editor
  Bundle ID:        com.example.myapp
  App ID:           6761651599
  Primary Locale:   en-GB

Version 1.0 - PREPARE_FOR_SUBMISSION
────────────────────────────────────────

✅ App Name              MyApp - Smart Photo Editor
✅ Description           1,794 characters
✅ Keywords              99/100 characters
✅ Support URL           https://example.com/myapp
✅ Privacy Policy URL    https://example.com/myapp/privacy
✅ Copyright             2026 Your Company
✅ Content Rights        DOES_NOT_USE_THIRD_PARTY_CONTENT
✅ Primary Category      PHOTO_AND_VIDEO
✅ Age Rating            Configured
✅ Pricing               Free
✅ Review Contact        Your Name
✅ App Icon              Configured
✅ iPhone Screenshots    5 screenshot(s)
❌ iPad Screenshots      Missing → Fix
⚠️ Privacy Labels        Not published → Open in Web
❌ Build                 Not attached → Fix

Summary: 14/17 items complete
Missing: iPad Screenshots, Privacy Labels, Build
```

## Implementation

```python
import jwt, time, json, os, urllib.request

def generate_token():
    with open(os.path.expanduser("~/.aso/credentials.json")) as f:
        creds = json.load(f)
    with open(os.path.expanduser(creds["privateKeyPath"])) as f:
        pk = f.read()
    return jwt.encode(
        {"iss": creds["issuerId"], "iat": int(time.time()), "exp": int(time.time())+1200, "aud": "appstoreconnect-v1"},
        pk, algorithm="ES256", headers={"kid": creds["keyId"], "typ": "JWT"}
    )

def api(method, endpoint, token, data=None):
    url = f"https://api.appstoreconnect.apple.com/v1/{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def check_readiness(app_id):
    token = generate_token()
    results = []

    # Get app info
    app = api("GET", f"apps/{app_id}?include=appInfos,appStoreVersions", token)
    results.append(("App Name", app["data"]["attributes"]["name"], True))

    # Get version in PREPARE_FOR_SUBMISSION
    versions = api("GET", f"apps/{app_id}/appStoreVersions?filter[appStoreState]=PREPARE_FOR_SUBMISSION", token)
    if not versions["data"]:
        return [("Version", "No version ready for submission", False)]

    version = versions["data"][0]
    version_id = version["id"]

    # Get localizations
    locs = api("GET", f"appStoreVersions/{version_id}/appStoreVersionLocalizations", token)
    for loc in locs["data"]:
        attrs = loc["attributes"]
        locale = attrs["locale"]

        desc = attrs.get("description", "")
        results.append((f"Description ({locale})", f"{len(desc)} chars", bool(desc)))

        kw = attrs.get("keywords", "")
        results.append((f"Keywords ({locale})", f"{len(kw)}/100 chars", bool(kw)))

        results.append((f"Support URL ({locale})", attrs.get("supportUrl", "Missing"), bool(attrs.get("supportUrl"))))

    # Check screenshots
    for loc in locs["data"]:
        locale = loc["attributes"]["locale"]
        ss_sets = api("GET", f"appStoreVersionLocalizations/{loc['id']}/appScreenshotSets", token)

        iphone_count = 0
        ipad_count = 0
        for ss_set in ss_sets["data"]:
            display = ss_set["attributes"]["screenshotDisplayType"]
            screenshots = api("GET", f"appScreenshotSets/{ss_set['id']}/appScreenshots", token)
            count = len(screenshots["data"])

            if "IPHONE" in display:
                iphone_count += count
            elif "IPAD" in display:
                ipad_count += count

        results.append((f"iPhone Screenshots ({locale})", f"{iphone_count} screenshot(s)", iphone_count > 0))
        results.append((f"iPad Screenshots ({locale})", f"{ipad_count} screenshot(s)" if ipad_count else "Missing", ipad_count > 0))

    # Check build
    builds = api("GET", f"apps/{app_id}/builds?limit=1&sort=-uploadedDate", token)
    has_build = len(builds["data"]) > 0
    results.append(("Build", builds["data"][0]["attributes"]["version"] if has_build else "Not uploaded", has_build))

    # Check age rating
    try:
        age = api("GET", f"appStoreVersions/{version_id}/ageRatingDeclaration", token)
        results.append(("Age Rating", "Configured", True))
    except:
        results.append(("Age Rating", "Not configured", False))

    return results

# Run check
APP_ID = "APP_ID_HERE"
results = check_readiness(APP_ID)

print("📱 Submission Readiness Check\n")
print("─" * 50)

passed = 0
failed = 0
for name, value, ok in results:
    icon = "✅" if ok else "❌"
    print(f"{icon} {name:30} {value}")
    if ok:
        passed += 1
    else:
        failed += 1

print("─" * 50)
print(f"\nSummary: {passed}/{passed+failed} items complete")
if failed > 0:
    print(f"Missing: {failed} item(s)")
```

## Required Checks

### App Identity
- [x] App Name
- [x] Bundle ID
- [x] App ID
- [x] Primary Locale

### Metadata (per locale)
- [x] Description (required)
- [x] Keywords (required)
- [ ] Promotional Text (optional)
- [x] Support URL (required)
- [x] Privacy Policy URL (required)
- [ ] Marketing URL (optional)

### App Info
- [x] Title (30 chars)
- [x] Subtitle (30 chars)
- [x] Copyright
- [x] Primary Category
- [x] Content Rights Declaration

### Assets
- [x] App Icon (1024x1024 in build)
- [x] iPhone Screenshots (required)
- [ ] iPad Screenshots (optional but recommended)
- [ ] App Preview Video (optional)

### Configuration
- [x] Age Rating
- [x] Pricing
- [x] Availability
- [x] Review Contact Info

### Privacy
- [ ] Privacy Nutrition Labels (iris API)

### Build
- [x] Build uploaded
- [x] Build attached to version

## Error Handling

### "No version in PREPARE_FOR_SUBMISSION"
Create a new version or check current version state.

### 401 Unauthorized
API key expired or invalid. Run `/aso-setup`.

### Missing credentials
Run `/aso-setup` to configure API key.
