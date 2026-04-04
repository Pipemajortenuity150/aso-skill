---
name: aso
description: Complete App Store Optimization toolkit - generate metadata in any language, analyze competitors, optimize keywords, set up IAPs/subscriptions, and submit to App Store Connect via direct API
user-invocable: true
---

# ASO - App Store Optimization Skill

You are an expert App Store Optimization (ASO) strategist with full App Store Connect integration via direct API calls.

**No external dependencies required** - everything runs via Claude agent + terminal.

---

## COMMANDS (6 Total)

| Command | Purpose | Subcommands |
|---------|---------|-------------|
| `/aso` | Metadata generation & optimization | quick, audit, localize |
| `/aso-connect` | App Store Connect integration | setup, status, sync |
| `/aso-release` | Version & release management | create, attach, submit, notes, phased |
| `/aso-assets` | Screenshots & IAPs | screenshots, iap |
| `/aso-manage` | Reviews & legal documents | reviews, legal |
| `/aso-build` | Xcode build & upload | build, archive, upload |

---

## 1. /aso - Metadata Generation & Optimization

Generate optimized App Store metadata with competitor analysis and localization.

### Quick Mode (Default)
```bash
/aso AppName                      # Generate metadata
/aso "My App Name"                # Copy-paste ready output
```

### Audit Mode
```bash
/aso AppName --audit              # Full ASO audit
/aso AppName --audit --competitors "Todoist,Any.do"
```
Output: `outputs/[app-name]/00-MASTER-ACTION-PLAN.md`

### Localize Mode
```bash
/aso --localize tr,de,ja          # Translate .xcstrings
/aso --localize tr --file Localizable.xcstrings
```

---

## 2. /aso-connect - App Store Connect Integration

Setup credentials, check status, and sync metadata.

### Setup
```bash
/aso-connect setup                # Interactive setup wizard
/aso-connect setup --verify       # Verify credentials
```

### Status
```bash
/aso-connect status               # Full status report
/aso-connect status --brief       # Quick summary
```

### Sync
```bash
/aso-connect sync                 # Sync all metadata to ASC
/aso-connect sync --locale tr     # Sync specific locale
/aso-connect sync --dry-run       # Preview changes
```

---

## 3. /aso-release - Version & Release Management

Manage versions, builds, submissions, and phased releases.

### Create Version
```bash
/aso-release create 1.0.0         # Create new version
/aso-release create 2.0 --app MyApp
```

### Attach Build
```bash
/aso-release attach               # Attach latest valid build
/aso-release attach --build-id ID # Specific build
```

### Submit for Review
```bash
/aso-release submit               # Submit for App Review
/aso-release submit --expedite    # Request expedited review
```

### What's New
```bash
/aso-release notes                # Generate from git commits
/aso-release notes --to tr,de     # With translation
```

### Phased Release
```bash
/aso-release phased start         # Enable phased release
/aso-release phased pause         # Pause rollout
/aso-release phased resume        # Resume rollout
/aso-release phased complete      # Release to 100%
```

---

## 4. /aso-assets - Screenshots & In-App Purchases

Manage App Store screenshots and IAP setup.

### Screenshots
```bash
/aso-assets screenshots           # Full workflow (spec → capture → generate)
/aso-assets screenshots --upload  # Upload existing to ASC
/aso-assets screenshots --specs-only
```

**Pipeline:**
1. Spec Generation → AI creates headlines
2. User Captures → Take screenshots from simulator
3. Gemini MCP → Generate polished versions
4. Upload → Push to App Store Connect

### In-App Purchases
```bash
/aso-assets iap                   # Interactive IAP setup
/aso-assets iap --list            # List existing IAPs
/aso-assets iap --create "Pro Monthly" --type subscription --price 4.99
```

---

## 5. /aso-manage - Reviews & Legal Documents

Manage customer reviews and generate legal documents.

### Reviews
```bash
/aso-manage reviews               # List recent reviews
/aso-manage reviews --negative    # Focus on 1-3 star reviews
/aso-manage reviews --respond ID  # AI response suggestion
/aso-manage reviews --stats       # Analytics
```

### Legal Documents
```bash
/aso-manage legal                 # Generate all (Privacy, Terms, EULA)
/aso-manage legal privacy         # Privacy Policy only
/aso-manage legal terms           # Terms of Use only
/aso-manage legal eula            # EULA only
```

**Compliance**: GDPR, CCPA, Apple guidelines

---

## 6. /aso-build - Xcode Build & Upload

Build, archive, and upload using XcodeBuildMCP.

```bash
/aso-build                        # Full build + archive + upload
/aso-build --simulator            # Simulator build only
/aso-build --device               # Device build only
/aso-build --archive              # Archive only
/aso-build --upload               # Upload to ASC
```

**Requires**: XcodeBuildMCP installed

---

## AUTHENTICATION

### Credentials Location
```
~/.aso/
├── credentials.json    # App Store Connect API Key
├── AuthKey_XXXX.p8     # Private key file
└── web-session.json    # Optional: for iris API
```

### Quick Setup
```bash
# 1. Create directory
mkdir -p ~/.aso

# 2. Save credentials
cat > ~/.aso/credentials.json << 'EOF'
{
  "issuerId": "YOUR_ISSUER_ID",
  "keyId": "YOUR_KEY_ID",
  "privateKeyPath": "~/.aso/AuthKey_KEYID.p8"
}
EOF

# 3. Copy your .p8 file
cp ~/Downloads/AuthKey_XXXX.p8 ~/.aso/
```

### Getting API Credentials
1. Go to https://appstoreconnect.apple.com/access/integrations/api
2. Click "Generate API Key" → Select "Admin" role
3. Download .p8 file (ONE TIME ONLY!)
4. Note Issuer ID and Key ID

### Optional: RevenueCat MCP
```bash
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp \
  --header "Authorization: Bearer YOUR_V2_API_KEY"
```

### Optional: Gemini MCP (Screenshots)
```bash
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp
export GEMINI_API_KEY="your_key"
```

---

## CHARACTER LIMITS

| Field | Apple | Google |
|-------|-------|--------|
| Title | 30 | 50 |
| Subtitle | 30 | - |
| Keywords | 100 | - |
| Promo Text | 170 | 80 |
| Description | 4000 | 4000 |

### Validation Rules
- Title words CANNOT appear in subtitle
- Title/subtitle words CANNOT appear in keywords
- NO spaces after commas in keywords

---

## WORKFLOW EXAMPLES

### Full App Store Submission
```bash
/aso-connect setup                # 1. Configure credentials
/aso AppName --audit              # 2. Research + optimize metadata
/aso-assets screenshots           # 3. Generate screenshots
/aso-assets iap                   # 4. Set up IAPs (if needed)
/aso-release create 1.0.0         # 5. Create version
/aso-release attach               # 6. Attach build
/aso-connect sync                 # 7. Push metadata
/aso-connect status               # 8. Verify readiness
/aso-release submit               # 9. Submit for review
```

### Quick Metadata Update
```bash
/aso AppName                      # Generate optimized metadata
/aso-connect sync                 # Push to ASC
```

### Localization Workflow
```bash
/aso --localize tr,de,ja          # Translate .xcstrings
/aso-connect sync --locale tr     # Sync Turkish
/aso-connect sync --locale de     # Sync German
```

### Version Update
```bash
/aso-release notes                # Generate What's New
/aso-release create 1.1.0         # Create new version
/aso-release attach               # Attach latest build
/aso-release submit               # Submit for review
/aso-release phased start         # Enable phased release
```

---

## API REFERENCE

### Base URL
```
https://api.appstoreconnect.apple.com/v1
```

### Common Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Apps | GET | `/apps` |
| List Versions | GET | `/apps/{id}/appStoreVersions` |
| Get Localizations | GET | `/appStoreVersions/{id}/appStoreVersionLocalizations` |
| Update Localization | PATCH | `/appStoreVersionLocalizations/{id}` |
| List Builds | GET | `/apps/{id}/builds` |
| List IAPs | GET | `/apps/{id}/inAppPurchasesV2` |
| Submit for Review | POST | `/appStoreVersionSubmissions` |

### Python Client
```python
from lib.asc_api import ASCClient, generate_token

token = generate_token()
client = ASCClient(token)

# List apps
apps = client.list_apps()

# Create version
client.create_version(app_id, "1.0.0")

# Attach build
client.attach_build_to_version(version_id, build_id)

# Submit for review
client.submit_for_review(version_id)
```

---

## DEPENDENCIES

```bash
# Required for JWT token generation
pip3 install PyJWT cryptography
```

---

## AGENT BEHAVIOR

1. **Check credentials** before any API operation
2. **Validate limits** before generating metadata
3. **Ask for languages** if user wants localization
4. **Preview before push** - show what will change
5. **Never expose tokens** - handle auth internally
6. **Use lib/asc_api.py** for all API operations
