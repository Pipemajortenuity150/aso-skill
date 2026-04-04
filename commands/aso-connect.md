# /aso-connect - App Store Connect Integration

Setup, status checking, and data synchronization with App Store Connect.

## Usage

```bash
/aso-connect setup                # Initial setup wizard
/aso-connect status               # Check app status
/aso-connect sync                 # Sync metadata to ASC
```

## Subcommands

### setup - Initial Configuration

```bash
/aso-connect setup                # Interactive setup
/aso-connect setup --verify       # Verify existing credentials
```

**Setup Flow:**
```
1. API Key Configuration
   → Key ID, Issuer ID, Private Key (.p8)

2. App Selection
   → List apps, select target

3. Credential Storage
   → ~/.aso/credentials.json

4. Connection Test
   → Verify API access
```

### status - App Status Check

```bash
/aso-connect status               # Full status report
/aso-connect status --brief       # Quick summary
/aso-connect status --app MyApp   # Specific app
```

**Status Report:**
```
📱 MyApp - Status Report
─────────────────────────────────────────

Version: 1.2.0 (READY_FOR_SALE)
Next: 1.3.0 (PREPARE_FOR_SUBMISSION)

Build: 1.3.0 (45) - VALID ✅
Processing: None

Metadata Completeness:
├── Title: ✅ 28/30 chars
├── Subtitle: ✅ 25/30 chars
├── Keywords: ✅ 95/100 chars
├── Description: ✅ 3200/4000 chars
├── Screenshots: ✅ 6/6
└── Privacy URL: ✅

Locales: en-US ✅, tr ✅, de ⚠️ (missing keywords)

Last Review: Approved (2 days ago)
```

### sync - Metadata Synchronization

```bash
/aso-connect sync                 # Sync all metadata
/aso-connect sync --field title   # Sync specific field
/aso-connect sync --locale tr     # Sync specific locale
/aso-connect sync --dry-run       # Preview changes
```

**Sync Fields:**
- `title` - App name
- `subtitle` - Subtitle
- `keywords` - Search keywords
- `description` - Full description
- `whatsnew` - Release notes
- `promo` - Promotional text
- `all` - Everything (default)

---

## Credentials Setup

### Required Information

```
Key ID:        XXXXXXXXXX (10 chars)
Issuer ID:     xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Private Key:   AuthKey_XXXXXXXXXX.p8
```

### Getting API Credentials

1. Go to App Store Connect → Users and Access → Keys
2. Generate new API Key (Admin role)
3. Download .p8 file (one-time only!)
4. Note Key ID and Issuer ID

### Storage Location

```
~/.aso/
├── credentials.json    # API credentials
└── config.json         # App preferences
```

**credentials.json:**
```json
{
  "key_id": "XXXXXXXXXX",
  "issuer_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "key_path": "~/.aso/AuthKey_XXXXXXXXXX.p8"
}
```

---

## Implementation

```python
from lib.asc_api import ASCClient, generate_token

# Generate JWT token
token = generate_token()

# Initialize client
client = ASCClient(token)

# List apps
apps = client.list_apps()
for app in apps:
    print(f"{app['attributes']['name']} ({app['id']})")

# Get app status
app_id = apps[0]["id"]
versions = client.list_versions(app_id)
current = next(v for v in versions
               if v["attributes"]["appStoreState"] == "READY_FOR_SALE")

# Update metadata
client.update_localization(
    loc_id=loc_id,
    title="New Title",
    subtitle="New Subtitle",
    keywords="new,keywords,here"
)
```

---

## Pre-Flight Checks

Before sync, the system verifies:

- [ ] API credentials valid
- [ ] App exists and accessible
- [ ] Version in editable state
- [ ] Character limits respected
- [ ] Required fields filled

---

## Examples

```bash
# First-time setup
/aso-connect setup

# Check submission readiness
/aso-connect status

# Sync Turkish metadata
/aso-connect sync --locale tr

# Preview sync changes
/aso-connect sync --dry-run

# Verify credentials work
/aso-connect setup --verify
```

---

## Troubleshooting

### Common Issues

**"Invalid credentials"**
- Verify Key ID is correct (10 characters)
- Check Issuer ID format (UUID)
- Ensure .p8 file is valid and accessible

**"App not found"**
- Verify app exists in App Store Connect
- Check API key has access to the app
- Try `/aso-connect setup` to re-select app

**"Version not editable"**
- Version may be in review or already live
- Create new version with `/aso-release create X.Y.Z`

