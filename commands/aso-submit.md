# /aso-submit Command

Submit app to App Store Connect with metadata, privacy labels, and screenshots.

## Trigger
- `/aso-submit` or `/aso-submit AppName`
- "submit to app store", "push metadata", "deploy to ASC"

## Prerequisites
- Blitz installed with web session
- App created in App Store Connect
- Build uploaded and attached to version
- Metadata generated (via `/aso` or `/aso-audit`)

## Workflow

### 1. Check Authentication
```bash
test -f ~/.blitz/asc-agent/web-session.json && echo "✅ Session" || echo "❌ No session - run /aso-setup"
```

### 2. Get App Info
```bash
asc apps list | grep -i "APP_NAME"
# Note APP_ID for subsequent commands
```

### 3. Privacy Labels

**Ask user about data collection:**
- Does app collect data? → If no, use empty declaration
- What data? (crash, analytics, user accounts, etc.)
- Linked to user? Tracking?

**Apply privacy labels:**
```bash
# Create declaration
cat > /tmp/privacy.json << 'EOF'
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
EOF

# Preview
asc web privacy plan --app "APP_ID" --file /tmp/privacy.json --pretty

# Apply
asc web privacy apply --app "APP_ID" --file /tmp/privacy.json --allow-deletes --confirm

# Publish (REQUIRED!)
asc web privacy publish --app "APP_ID" --confirm
```

### 4. Metadata Push (Multi-Language)

**Convert ASO metadata to Blitz format:**

Create directory structure:
```
metadata/
├── app-info/
│   ├── en-GB.json
│   ├── tr.json
│   ├── de-DE.json
│   └── ...
└── version/
    └── 1.0/
        ├── en-GB.json
        ├── tr.json
        ├── de-DE.json
        └── ...
```

**app-info/{locale}.json:**
```json
{
  "name": "App Title (30 chars)",
  "subtitle": "App Subtitle (30 chars)",
  "privacyPolicyUrl": "https://..."
}
```

**version/{version}/{locale}.json:**
```json
{
  "description": "Full description (4000 chars)...",
  "keywords": "keyword1,keyword2,keyword3 (100 chars)",
  "promotionalText": "Promo text (170 chars)...",
  "marketingUrl": "https://...",
  "supportUrl": "https://..."
}
```

**Push to ASC:**
```bash
# Dry run first
asc metadata push --app "APP_ID" --version "1.0" --dir ./metadata --dry-run

# Apply
asc metadata push --app "APP_ID" --version "1.0" --dir ./metadata
```

### 5. Screenshots (Optional)

```bash
# List existing
asc screenshots list --app "APP_ID"

# Upload new
asc screenshots upload \
  --localization-id "LOCALIZATION_ID" \
  --display-type "APP_IPHONE_67" \
  --path ./screenshots/
```

Display types:
- `APP_IPHONE_67` - iPhone 6.7" (1290x2796)
- `APP_IPHONE_65` - iPhone 6.5" (1242x2688)
- `APP_IPHONE_55` - iPhone 5.5" (1242x2208)

### 6. IAP Attachment (If Applicable)

If app has IAPs/subscriptions in READY_TO_SUBMIT:
```bash
# Run /aso-iap or use iris API directly
```

### 7. Verify Submission Readiness

```bash
asc versions list --app "APP_ID"
# Check version state and missing items
```

### 8. Submit for Review

Via ASC web UI or:
```bash
asc versions submit --app "APP_ID" --version "VERSION_ID"
```

## Quick Checklist

Before `/aso-submit`:
- [ ] Build uploaded
- [ ] App icon (1024x1024) uploaded
- [ ] Screenshots ready
- [ ] Metadata generated
- [ ] Privacy policy URL live
- [ ] Support URL live

During `/aso-submit`:
- [ ] Privacy labels applied
- [ ] Privacy labels published
- [ ] Metadata pushed (all languages)
- [ ] Screenshots uploaded
- [ ] IAPs attached (if any)

After:
- [ ] Submit for review
- [ ] Monitor status

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

### 401 Session Expired
```
Call asc_web_auth MCP tool to re-authenticate
```

### Metadata validation failed
Check character limits and duplicate keywords.

### Screenshot upload failed
Verify dimensions and file format (PNG/JPEG).

## Agent Notes

- Always preview before applying (`--dry-run`, `plan`)
- Always publish after privacy apply
- Convert ASO metadata format to Blitz JSON format
- Support any number of languages
- Confirm each step with user
- Never print session cookies
