# /aso-assets - Screenshots & In-App Purchases

Manage App Store screenshots and in-app purchases.

## Usage

```bash
/aso-assets screenshots           # Generate screenshots
/aso-assets screenshots --upload  # Upload to ASC
/aso-assets iap                   # Setup IAPs
/aso-assets iap --list            # List existing IAPs
```

## Subcommands

### screenshots - Screenshot Generation

```bash
/aso-assets screenshots                    # Full workflow
/aso-assets screenshots --upload           # Upload existing
/aso-assets screenshots --specs-only       # Just generate specs
```

**Pipeline:**
```
1. Spec Generation → AI creates headlines
2. User Captures → Take screenshots from simulator
3. Gemini MCP → Generate polished versions
4. Upload → Push to App Store Connect
```

### iap - In-App Purchases

```bash
/aso-assets iap                   # Interactive setup
/aso-assets iap --list            # List existing
/aso-assets iap --create          # Create new IAP
```

---

## Screenshot Workflow

### Phase 1: Spec Generation
Agent analyzes codebase, creates headline specs:

```
📋 Screenshot Specs:

1. "TRACK TRADING CARD PRICES"
   → Screenshot: Price tracking screen

2. "SEARCH ANY CARD INSTANTLY"
   → Screenshot: Search results

3. "BUILD YOUR COLLECTION"
   → Screenshot: Collection view
```

**Good Specs:**
```
✅ TRACK TRADING CARD PRICES
✅ SEARCH ANY VERSE IN SECONDS
✅ BUILD YOUR DREAM WORKOUT
```

**Bad Specs:**
```
❌ MANAGE YOUR STUFF (generic)
❌ EASY TO USE (vague)
```

### Phase 2: User Captures
User takes screenshots from simulator:
- Full data states (not empty)
- Clean status bar (9:41, full battery)
- Consistent mode (all light or all dark)

### Phase 3: Gemini MCP Generation

```
Prompt to Gemini:
"Create App Store screenshot with:
- Bold red (#E31837) background
- 'TRACK TRADING CARD PRICES' headline
- iPhone 15 Pro frame with this screenshot
- 1290x2796 pixels"
```

Generates 3 versions per spec → User picks favorite.

### Phase 4: Upload to ASC

```python
from lib.asc_api import ASCClient, generate_token

client = ASCClient(generate_token())

# Create screenshot set
ss_set = client.create_screenshot_set(loc_id, "APP_IPHONE_67")

# Reserve upload
reservation = client.reserve_screenshot(ss_set["id"], "01.jpg", file_size)

# Upload to Apple S3
# ... upload logic ...

# Commit
client.commit_screenshot(screenshot_id, checksum)
```

---

## Screenshot Dimensions

| Display | Dimensions |
|---------|------------|
| iPhone 6.5" | 1242 x 2688 |
| iPhone 6.7" | 1290 x 2796 |
| iPhone 6.9" | 1320 x 2868 |
| iPad Pro 12.9" | 2048 x 2732 |

**Default: iPhone 6.7" (1290 x 2796)**

---

## IAP Workflow

### Common Patterns

**Credit Packs (Consumable):**
```
com.app.credits.5   →  5 credits  → $0.99
com.app.credits.15  → 15 credits  → $1.99
com.app.credits.50  → 50 credits  → $4.99
```

**Subscriptions:**
```
com.app.pro.monthly → $4.99/month
com.app.pro.yearly  → $39.99/year
com.app.lifetime    → $99.99 one-time
```

### Create IAP

```python
client.create_iap(
    app_id=app_id,
    product_id="com.myapp.pro.monthly",
    name="Pro Monthly",
    iap_type="AUTO_RENEWABLE_SUBSCRIPTION"
)
```

### IAP Types

| Type | Use Case |
|------|----------|
| `CONSUMABLE` | Credits, coins |
| `NON_CONSUMABLE` | Lifetime unlock |
| `AUTO_RENEWABLE_SUBSCRIPTION` | Monthly/yearly |
| `NON_RENEWING_SUBSCRIPTION` | Season pass |

---

## Prerequisites

### For Screenshots
```bash
# Gemini MCP
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp
export GEMINI_API_KEY="your_key"
```

### For IAP
```bash
# ASC credentials
cat ~/.aso/credentials.json
```

---

## Examples

```bash
# Full screenshot workflow
/aso-assets screenshots

# Upload existing screenshots
/aso-assets screenshots --upload --dir screenshots/final/

# List IAPs
/aso-assets iap --list

# Create subscription
/aso-assets iap --create "Pro Monthly" --type subscription --price 4.99
```

---

## Output Structure

```
screenshots/
├── 01-track-prices/
│   ├── simulator.png       # User's screenshot
│   ├── v1.jpg, v2.jpg, v3.jpg  # Gemini versions
│   └── final.jpg           # Selected
├── final/
│   ├── 01-track-prices.jpg
│   └── 02-search-cards.jpg
└── showcase.png            # Preview
```
