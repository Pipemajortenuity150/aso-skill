# CLAUDE.md

This file provides guidance to Claude Code when working with this ASO skill.

## What This Is

A comprehensive **App Store Optimization (ASO) skill** for Claude Code with 6 consolidated commands:

| Command | Purpose |
|---------|---------|
| `/aso` | Metadata generation (quick + audit + localize) |
| `/aso-connect` | App Store Connect (setup + status + sync) |
| `/aso-release` | Version management (create + attach + submit + notes + phased) |
| `/aso-assets` | Assets (screenshots + iap) |
| `/aso-manage` | Management (reviews + legal) |
| `/aso-build` | Xcode (build + archive + upload) |

## Architecture

```
aso-skill/
├── SKILL.md              # Main skill definition (user-invocable)
├── CLAUDE.md             # This file
├── agents/
│   ├── aso-quick.md      # Fast metadata agent (sonnet)
│   ├── aso-full.md       # Full audit orchestrator (opus)
│   └── asc-api.md        # ASC API agent
├── commands/
│   ├── aso.md            # /aso (metadata + audit + localize)
│   ├── aso-connect.md    # /aso-connect (setup + status + sync)
│   ├── aso-release.md    # /aso-release (version + build + submit)
│   ├── aso-assets.md     # /aso-assets (screenshots + iap)
│   ├── aso-manage.md     # /aso-manage (reviews + legal)
│   └── aso-build.md      # /aso-build (xcode)
├── lib/
│   ├── itunes_api.py     # iTunes Search API client
│   ├── keyword_engine.py # Keyword analysis engine
│   └── asc_api.py        # App Store Connect API client
└── templates/
    ├── apple-metadata.md  # Apple App Store template
    └── google-metadata.md # Google Play Store template
```

## Installation

### User-Level (All Projects)
```bash
cp -r aso-skill ~/.claude/skills/aso
```

### Project-Level
```bash
cp -r aso-skill /path/to/project/.claude/skills/aso
```

### Verification
```bash
ls ~/.claude/skills/aso/
# Should show: SKILL.md, agents/, commands/, lib/, templates/
```

## Credentials

All credentials stored at `~/.aso/`:

```
~/.aso/
├── credentials.json    # API Key (issuerId, keyId, privateKeyPath)
├── AuthKey_XXXX.p8     # Private key file
└── web-session.json    # Optional: for iris API features

# RevenueCat: Uses MCP server (cloud-hosted, no local file)
# Install: claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer V2_KEY"

# Gemini MCP (Screenshots)
# Install: claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp
# Set: export GEMINI_API_KEY="your_key"
```

### API Key Authentication
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

## Key Design Decisions

### Multi-Source Data Strategy
1. **iTunes Search API** - Free, official, primary source
2. **WebFetch scraping** - Fallback for additional data
3. **Astro MCP** - Optional real-time rankings (if configured)
4. **User input** - Last resort for unavailable data

### Platform-Specific Limits (CRITICAL)
```yaml
apple:
  title: 30
  subtitle: 30
  promotional_text: 170
  keywords: 100
  description: 4000

google:
  title: 50
  short_description: 80
  full_description: 4000
```

### No Keyword Duplication Rule
- Words in title CANNOT appear in subtitle
- Words in title/subtitle CANNOT appear in keyword field
- Validate before every output

### Memory Persistence
The skill saves state to Claude Code memory:
- App details and preferences
- Confirmed benefits and keywords
- Screenshot pairings and assessments
- Generated metadata

This enables resuming across conversations.

## Python Modules

### asc_api.py (Primary)
```python
from lib.asc_api import ASCClient, generate_token

token = generate_token()
client = ASCClient(token)

# Core operations
apps = client.list_apps()
client.create_version(app_id, "1.0.0")
client.attach_build_to_version(version_id, build_id)
client.submit_for_review(version_id)
client.create_phased_release(version_id)

# Metadata
client.update_localization(loc_id, title="...", subtitle="...", keywords="...")

# Screenshots
client.create_screenshot_set(loc_id, "APP_IPHONE_67")
client.reserve_screenshot(set_id, "01.jpg", file_size)
client.commit_screenshot(screenshot_id, checksum)
```

Requires PyJWT: `pip3 install PyJWT cryptography`

### itunes_api.py
```python
from lib.itunes_api import iTunesAPI

api = iTunesAPI()
apps = api.search_apps("productivity", limit=10)
analysis = api.analyze_competitors(["Todoist", "Any.do"])
```

No external dependencies. Uses urllib only.

### keyword_engine.py
```python
from lib.keyword_engine import KeywordEngine

engine = KeywordEngine()
analysis = engine.analyze_keywords(
    seed_keywords=["task manager"],
    app_features=["AI scheduling"],
    app_name="TaskFlow"
)
```

Returns prioritized keywords with placement recommendations.

## Command Reference

| Command | Subcommands | Purpose |
|---------|-------------|---------|
| `/aso` | (default), --audit, --localize | Metadata generation & optimization |
| `/aso-connect` | setup, status, sync | ASC integration |
| `/aso-release` | create, attach, submit, notes, phased | Version & release management |
| `/aso-assets` | screenshots, iap | Screenshots & IAP setup |
| `/aso-manage` | reviews, legal | Reviews & legal docs |
| `/aso-build` | (default), --simulator, --archive, --upload | Xcode build & upload |

## Workflow Patterns

### Full App Store Submission
```
/aso-connect setup                # Configure credentials
/aso AppName --audit              # Research + optimize
/aso-assets screenshots           # Generate screenshots
/aso-assets iap                   # Set up IAPs
/aso-release create 1.0.0         # Create version
/aso-release attach               # Attach build
/aso-connect sync                 # Push metadata
/aso-connect status               # Verify readiness
/aso-release submit               # Submit for review
```

### Version Update
```
/aso-release notes                # Generate What's New
/aso-release create 1.1.0         # Create new version
/aso-release attach               # Attach latest build
/aso-release submit               # Submit for review
/aso-release phased start         # Enable phased release
```

### Quick Metadata
```
/aso AppName                      # Generate optimized metadata
/aso-connect sync                 # Push to ASC
```

### Localization
```
/aso --localize tr,de,ja          # Translate .xcstrings
/aso-connect sync --locale tr     # Sync specific locale
```

## API Endpoints

### Public API (JWT Auth)
Base URL: `https://api.appstoreconnect.apple.com/v1`

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Apps | GET | `/apps` |
| List Versions | GET | `/apps/{id}/appStoreVersions` |
| Create Version | POST | `/appStoreVersions` |
| List Builds | GET | `/apps/{id}/builds` |
| Attach Build | PATCH | `/appStoreVersions/{id}` |
| Get Localizations | GET | `/appStoreVersions/{id}/appStoreVersionLocalizations` |
| Update Localization | PATCH | `/appStoreVersionLocalizations/{id}` |
| Submit for Review | POST | `/appStoreVersionSubmissions` |
| Create Phased Release | POST | `/appStoreVersionPhasedReleases` |
| List IAPs | GET | `/apps/{id}/inAppPurchasesV2` |
| List Reviews | GET | `/apps/{id}/customerReviews` |

### iris API (Web Session)
Base URL: `https://appstoreconnect.apple.com/iris/v1`

Used for:
- Privacy nutrition labels
- IAP/Subscription attachment to version
- Features not in public API

## Integration Points

### Gemini MCP (Screenshots)
- Required for screenshot generation
- Install: `claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp`
- Set: `export GEMINI_API_KEY="your_key"`
- Tools: `generate_image`, `edit_image`

### RevenueCat MCP (IAP Sync)
- Optional for IAP synchronization
- Install: `claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer V2_KEY"`
- Tools: `list_products`, `create_product`, `get_project`

### XcodeBuildMCP (Build)
- Required for /aso-build command
- Install: See https://github.com/getsentry/XcodeBuildMCP
- Tools: `build`, `archive`, `upload_to_testflight`

### Astro MCP (Optional)
- Real-time keyword rankings
- Tools: `list_apps`, `get_app_keywords`, `search_rankings`

## Quality Standards

### Output Requirements
- All character limits validated (100% compliance)
- No keyword duplication across fields
- Copy-paste ready (no placeholders)
- Specific dates in timelines (not "Week 1")
- Actionable checklists (not vague tasks)

### Self-Assessment
Each output should score >= 4/5 on:
- Completeness
- Actionability
- Data Quality
- User Readiness

## Troubleshooting

### iTunes API Timeout
- Retry after 5 seconds
- Fall back to WebFetch
- Ask user for competitor data

### Character Limit Exceeded
- Truncate intelligently (not mid-word)
- Suggest alternative phrasing
- Prioritize high-value keywords

### ASC Authentication Failed
- Check ~/.aso/credentials.json
- Verify API key is Admin role
- Regenerate token

### Screenshot Generation Failed
- Check Gemini MCP installed
- Check GEMINI_API_KEY environment variable set
- Verify simulator screenshot path exists

## Sources and Credits

This skill combines best practices from:
- [alirezarezvani/claude-code-aso-skill](https://github.com/alirezarezvani/claude-code-aso-skill) - Agent system, structured outputs
- [Mehrozsheikh/aso-appstore-listing-skill](https://github.com/Mehrozsheikh/aso-appstore-listing-skill) - Minimal skill format, Astro MCP
- [adamlyttleapps/claude-skill-aso-appstore-screenshots](https://github.com/adamlyttleapps/claude-skill-aso-appstore-screenshots) - Screenshot generation
