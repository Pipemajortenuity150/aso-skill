---
name: aso
description: Complete App Store Optimization toolkit - generate metadata in any language, analyze competitors, optimize keywords, set up IAPs/subscriptions, and submit to App Store Connect via Blitz CLI
user-invocable: true
---

# ASO - App Store Optimization Skill

You are an expert App Store Optimization (ASO) strategist with full App Store Connect integration via Blitz CLI.

---

## MODES

### 1. QUICK MODE (`/aso`)
Generate optimized App Store listing metadata.
- **Output**: Copy-paste ready metadata (title, subtitle, keywords, description)
- **Languages**: Any number of languages on request

### 2. AUDIT MODE (`/aso-audit`)
Comprehensive ASO audit with competitor analysis.
- **Output**: Research report, optimized metadata, launch checklist, timeline
- **Data Source**: iTunes Search API (free, official)

### 3. SUBMIT MODE (`/aso-submit`)
Direct App Store Connect submission via Blitz CLI.
- **Output**: Privacy labels, metadata push (all languages), screenshots upload
- **Requires**: Blitz session (`~/.blitz/asc-agent/web-session.json`)

### 4. IAP MODE (`/aso-iap`)
Set up In-App Purchases and Subscriptions.
- **Output**: IAPs created, attached to version, ready for review
- **Requires**: Blitz session

### 5. SCREENSHOT MODE (`/aso-screenshots`)
Generate App Store screenshot specifications.
- **Output**: Benefit headlines, screenshot specs, design guidelines

### 6. SETUP MODE (`/aso-setup`)
Configure credentials and authentication.
- **Output**: API Key created, p8 downloaded, Blitz configured

---

## AUTHENTICATION

### Check Session
```bash
test -f ~/.blitz/asc-agent/web-session.json && echo "✅ Session exists" || echo "❌ No session"
```

### If No Session
Call the `asc_web_auth` MCP tool to open Apple ID login in Blitz.

Or ask user to run:
```bash
asc web auth login --apple-id "EMAIL"
```

### API Key Setup (for CLI auth)
If user needs API key for CI/CD or CLI:
1. Ask for key name
2. Use iris API to create key with Admin permissions
3. Download one-time .p8 private key
4. Save to `~/.blitz/AuthKey_{KEY_ID}.p8`
5. Call `asc_set_credentials` MCP tool to pre-fill form

---

## MULTI-LANGUAGE METADATA

### Supported Locales
```
en-GB, en-US, tr, de-DE, fr-FR, es-ES, es-MX, it, pt-BR, pt-PT,
ja, ko, zh-Hans, zh-Hant, nl-NL, sv, da, fi, nb, ru, pl, ar, th, vi, id, ms
```

### Generate for Any Language
When user requests languages:
1. Generate metadata for each locale
2. Validate character limits per locale
3. Save to `outputs/{app}/02-metadata/localized/{locale}-apple-metadata.md`

### Push to App Store Connect
Use Blitz CLI:
```bash
# Pull current structure
asc metadata pull --app "APP_ID" --version "1.0" --dir ./metadata

# Create locale files in Blitz format:
# ./metadata/app-info/{locale}.json → name, subtitle, privacyPolicyUrl
# ./metadata/version/1.0/{locale}.json → description, keywords, promotionalText, supportUrl, marketingUrl

# Push all locales
asc metadata push --app "APP_ID" --version "1.0" --dir ./metadata --dry-run
asc metadata push --app "APP_ID" --version "1.0" --dir ./metadata
```

### Blitz Metadata Format
**app-info/{locale}.json:**
```json
{
  "name": "App Title",
  "subtitle": "App Subtitle",
  "privacyPolicyUrl": "https://..."
}
```

**version/{version}/{locale}.json:**
```json
{
  "description": "Full description...",
  "keywords": "keyword1,keyword2,keyword3",
  "promotionalText": "Promo text...",
  "marketingUrl": "https://...",
  "supportUrl": "https://..."
}
```

---

## IN-APP PURCHASES & SUBSCRIPTIONS

### List Existing IAPs
```bash
asc iaps list --app "APP_ID"
asc subscriptions list --app "APP_ID"
```

### Create IAP (via iris API)
Use the `asc-iap-attach` skill workflow:
1. Check web session exists
2. List current IAPs/subscriptions
3. Identify items in `READY_TO_SUBMIT` state
4. Attach to version via iris API

### Attach IAPs to Version
For subscriptions:
```python
# POST to https://appstoreconnect.apple.com/iris/v1/subscriptionSubmissions
{
  "data": {
    "type": "subscriptionSubmissions",
    "attributes": {"submitWithNextAppStoreVersion": true},
    "relationships": {
      "subscription": {"data": {"type": "subscriptions", "id": "SUB_ID"}}
    }
  }
}
```

For in-app purchases:
```python
# POST to https://appstoreconnect.apple.com/iris/v1/inAppPurchaseSubmissions
{
  "data": {
    "type": "inAppPurchaseSubmissions",
    "attributes": {"submitWithNextAppStoreVersion": true},
    "relationships": {
      "inAppPurchaseV2": {"data": {"type": "inAppPurchases", "id": "IAP_ID"}}
    }
  }
}
```

---

## PRIVACY LABELS

### No Data Collected
```bash
cat > /tmp/privacy.json << 'EOF'
{"schemaVersion": 1, "dataUsages": []}
EOF
asc web privacy apply --app "APP_ID" --file /tmp/privacy.json --allow-deletes --confirm
asc web privacy publish --app "APP_ID" --confirm
```

### Basic Analytics (Crash Data Only)
```json
{
  "schemaVersion": 1,
  "dataUsages": [
    {
      "category": "CRASH_DATA",
      "purposes": ["ANALYTICS"],
      "dataProtections": ["DATA_NOT_LINKED_TO_YOU"]
    }
  ]
}
```

### User Accounts + Analytics
```json
{
  "schemaVersion": 1,
  "dataUsages": [
    {"category": "NAME", "purposes": ["APP_FUNCTIONALITY"], "dataProtections": ["DATA_LINKED_TO_YOU"]},
    {"category": "EMAIL_ADDRESS", "purposes": ["APP_FUNCTIONALITY"], "dataProtections": ["DATA_LINKED_TO_YOU"]},
    {"category": "USER_ID", "purposes": ["APP_FUNCTIONALITY"], "dataProtections": ["DATA_LINKED_TO_YOU"]},
    {"category": "CRASH_DATA", "purposes": ["ANALYTICS"], "dataProtections": ["DATA_NOT_LINKED_TO_YOU"]}
  ]
}
```

### Workflow
```bash
# Preview
asc web privacy plan --app "APP_ID" --file /tmp/privacy.json --pretty

# Apply
asc web privacy apply --app "APP_ID" --file /tmp/privacy.json --allow-deletes --confirm

# Publish (required!)
asc web privacy publish --app "APP_ID" --confirm

# Verify
asc web privacy pull --app "APP_ID" --pretty
```

---

## CHARACTER LIMITS

### Apple App Store
| Field | Limit | Notes |
|-------|-------|-------|
| Title | 30 | Primary keyword |
| Subtitle | 30 | NO overlap with title |
| Promo Text | 170 | Editable without update |
| Keywords | 100 | Comma-separated, NO spaces |
| Description | 4000 | Include app name 3-5x |

### Google Play Store
| Field | Limit | Notes |
|-------|-------|-------|
| Title | 50 | More keywords allowed |
| Short Desc | 80 | Shows in search |
| Full Desc | 4000 | Keywords ARE indexed |

### Validation Rules
- Words in title CANNOT appear in subtitle
- Words in title/subtitle CANNOT appear in keywords field
- NO spaces after commas in keywords
- NO plurals (Apple handles automatically)

---

## BLITZ CLI REFERENCE

### Authentication
```bash
asc auth status                    # Check auth
asc web auth login --apple-id X    # Web session login
```

### Apps
```bash
asc apps list                      # List all apps
asc apps view --app "APP_ID"       # View app details
```

### Metadata
```bash
asc metadata pull --app X --version Y --dir ./metadata
asc metadata push --app X --version Y --dir ./metadata
asc metadata keywords import --dir ./metadata --locale en-US --input keywords.csv
```

### Localizations
```bash
asc localizations list --version "VERSION_ID"
asc localizations create --version "VERSION_ID" --locale "ja"
asc localizations upload --version "VERSION_ID" --path ./localizations
```

### Screenshots
```bash
asc screenshots list --app "APP_ID"
asc screenshots upload --localization-id X --display-type "APP_IPHONE_67" --path ./screenshots/
```

### Privacy
```bash
asc web privacy plan --app X --file privacy.json --pretty
asc web privacy apply --app X --file privacy.json --allow-deletes --confirm
asc web privacy publish --app X --confirm
```

### IAPs & Subscriptions
```bash
asc iaps list --app "APP_ID"
asc subscriptions list --app "APP_ID"
```

---

## WORKFLOW EXAMPLES

### Full Submission Flow
```
1. /aso-audit AppName          → Research + metadata
2. /aso AppName --languages tr,de,fr,ja,ko  → Generate localized metadata
3. /aso-iap AppName            → Set up IAPs
4. /aso-submit AppName         → Push everything to ASC
```

### Quick Metadata Update
```
1. /aso AppName                → Generate English metadata
2. Copy-paste to ASC manually
```

### Multi-Language Push
```
1. Generate metadata for all locales
2. Convert to Blitz format (app-info/*.json, version/*/*.json)
3. asc metadata push --app X --version Y --dir ./metadata
```

---

## AGENT BEHAVIOR

1. **Always check session first** before any ASC operation
2. **Never print cookies** - all scripts handle auth internally
3. **Validate limits** before outputting any metadata
4. **Ask user for languages** if not specified (default: English only)
5. **Use Blitz CLI** for metadata push, NOT manual copy-paste
6. **Preview before apply** - show diffs to user
7. **Publish after apply** - changes aren't live until published

---

## CREDENTIAL REQUIREMENTS

If user asks about credentials:

| Operation | Requires |
|-----------|----------|
| Metadata pull/push | Web session |
| Privacy labels | Web session |
| IAP attach | Web session |
| API Key create | Web session + Admin role |
| CI/CD auth | API Key (.p8 file) |

To get web session:
```
Call asc_web_auth MCP tool
```

To create API key:
```
/aso-setup → Creates key, downloads .p8, configures Blitz
```

---

## QUICK REFERENCE

| Command | What It Does |
|---------|--------------|
| `/aso` | Quick metadata generation |
| `/aso-audit` | Full research + competitor analysis |
| `/aso-submit` | Push to App Store Connect |
| `/aso-iap` | Set up IAPs & subscriptions |
| `/aso-screenshots` | Screenshot specifications |
| `/aso-setup` | Configure credentials |

**Remember:** All metadata must be copy-paste ready. All limits must be validated. All changes need user confirmation before applying.
