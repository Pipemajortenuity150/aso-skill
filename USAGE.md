# Usage Guide

Complete guide to using ASO Skill for App Store Optimization.

---

## Quick Reference

| Command | Use Case | Time |
|---------|----------|------|
| `/aso` | Quick metadata | 2-5 min |
| `/aso-audit` | Full analysis | 20-30 min |
| `/aso-submit` | ASC submission | 5-10 min |
| `/aso-iap` | IAP setup | 5-10 min |
| `/aso-sync` | Project-ASC-RC sync | 2-5 min |
| `/aso-setup` | Configure credentials | 2 min |
| `/aso-status` | Check readiness | 1 min |
| `/aso-screenshots` | Generate screenshots | 15-30 min |

---

## Command 1: `/aso` - Quick Metadata

### Basic Usage

```
/aso [app-name]
```

### Examples

```
/aso TaskFlow
/aso "My Fitness App"
/aso TaskFlow - AI task manager for busy professionals
```

### What It Does

1. **Recalls** any saved app data from memory
2. **Collects** app details (if not provided)
3. **Generates** optimized metadata for Apple + Google
4. **Validates** character limits and duplications
5. **Iterates** based on your feedback
6. **Saves** approved listing to memory

### Output Format

```json
{
  "platform": "apple",
  "metadata": {
    "title": "TaskFlow - AI Task Manager",
    "title_chars": "28/30",
    "subtitle": "Smart Productivity & Focus",
    "subtitle_chars": "26/30",
    "keywords": "productivity,organize,planner...",
    "keywords_chars": "95/100",
    "description": "...",
    "description_chars": "2847/4000"
  }
}
```

### Iteration Options

After generation:
- **Tone:** "Make it more premium"
- **Keywords:** "Focus on AI features"
- **Field:** "Rewrite the subtitle"
- **Save:** "Looks good, save it"

---

## Command 2: `/aso-audit` - Full Audit

### Basic Usage

```
/aso-audit [app-name]
```

### Examples

```
/aso-audit FitFlow
/aso-audit "MyApp" --competitors "Todoist,Any.do"
```

### What It Does

**Phase 1: Research (10-15 min)**
- Fetch competitor data via iTunes API
- Analyze keywords from top 5 competitors
- Identify market gaps and opportunities

**Phase 2: Optimization (5-10 min)**
- Generate Apple metadata (validated)
- Generate Google metadata (validated)
- Create visual assets specification

**Phase 3: Strategy (5-10 min)**
- Build pre-launch checklist (47 items)
- Create timeline with specific dates
- Generate review response templates

**Phase 4: Synthesis (5 min)**
- Consolidate all outputs
- Create master action plan

### Output Structure

```
outputs/[app-name]/
├── 00-MASTER-ACTION-PLAN.md      # START HERE
├── 01-research/
│   ├── keyword-list.md
│   ├── competitor-analysis.md
│   └── market-gaps.md
├── 02-metadata/
│   ├── apple-metadata.md         # Copy-paste ready
│   ├── google-metadata.md        # Copy-paste ready
│   └── visual-assets-spec.md
├── 03-launch/
│   ├── prelaunch-checklist.md
│   └── timeline.md
└── 04-optimization/
    ├── review-templates.md
    └── ongoing-tasks.md
```

### Using the Output

1. Open `00-MASTER-ACTION-PLAN.md`
2. Follow phases in order (01 → 02 → 03 → 04)
3. Check boxes as you complete tasks
4. Copy metadata from `02-metadata/`

---

## Command 3: `/aso-submit` - App Store Connect

### Prerequisites

- API Key configured (`~/.aso/credentials.json`)
- App already created in ASC
- Build uploaded

### Basic Usage

```
/aso-submit [app-name]
/aso-submit [app-name] --app-id 1234567890
```

### What It Does

1. **Checks** authentication status
2. **Configures** privacy nutrition labels
3. **Applies** metadata to App Store Connect
4. **Verifies** changes applied correctly

### Privacy Labels Options

```yaml
No data collected:
  → Empty declaration

Basic analytics:
  → Crash data (not linked)

User accounts:
  → Name, email (linked)
  → Crash data (not linked)
```

### Example Workflow

```
/aso-submit FitFlow

1. ✓ Checking authentication...
2. ✓ API Key valid

3. 📋 Privacy Labels
   Does your app collect data? [Yes/No]

4. ⏳ Applying privacy labels...
5. ✓ Labels published

6. 📝 Applying metadata...
7. ✓ Metadata applied

Ready to submit!
```

---

## Command 4: `/aso-status` - Check Readiness

### Basic Usage

```
/aso-status [app-name]
```

### What It Does

Checks all required items for App Store submission:

- App Name
- Description
- Keywords
- Support URL
- Privacy Policy URL
- Copyright
- Content Rights
- Primary Category
- Age Rating
- Pricing
- Review Contact
- App Icon
- iPhone Screenshots
- iPad Screenshots
- Privacy Nutrition Labels
- Build

### Output Example

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
❌ iPad Screenshots      Missing → Fix
⚠️ Privacy Labels        Not published → Open in Web
❌ Build                 Not attached → Fix

Summary: 14/17 items complete
Missing: iPad Screenshots, Privacy Labels, Build
```

---

## Command 5: `/aso-iap` - IAP Setup

### Prerequisites

- API Key configured
- App created in App Store Connect

### Basic Usage

```
/aso-iap [app-name]
```

### What It Does

1. **Lists** current IAPs and subscriptions
2. **Creates** new IAPs or subscriptions
3. **Attaches** items to current version
4. **Verifies** submission readiness

### Common IAP Patterns

```
Credit Packs (Consumable):
- 5 Credits: $0.99 (com.app.credits.5)
- 15 Credits: $1.99 (com.app.credits.15)
- 50 Credits: $4.99 (com.app.credits.50)

Subscriptions:
- Monthly Pro: $4.99/month
- Yearly Pro: $39.99/year (save 33%)
- Lifetime: $99.99 one-time
```

---

## Command 6: `/aso-setup` - Configure Credentials

### Basic Usage

```
/aso-setup
```

### What It Does

1. Guides you to create API Key in App Store Connect
2. Saves credentials to `~/.aso/credentials.json`
3. Tests API connection
4. Optionally configures web session for iris API

### Credentials Location

```
~/.aso/
├── credentials.json    # API Key info
├── AuthKey_XXXX.p8     # Private key file
└── web-session.json    # Optional: for iris API

# RevenueCat: Uses MCP server (no local file)
```

---

## Command 7: `/aso-sync` - Product Sync

### Prerequisites

- App Store Connect API Key configured
- RevenueCat MCP installed (optional)

### Basic Usage

```
/aso-sync
/aso-sync MyApp --app-id 1234567890
```

### What It Does

1. **Scans project** for IAP definitions (StoreKit config, Swift files)
2. **Creates products** in App Store Connect
3. **Syncs to RevenueCat** (via MCP) - products, entitlements, offerings

### Output Example

```
🔄 Syncing MyApp...
══════════════════════════════════════════════════

📂 Phase 1: Scanning project...
   Found 3 product(s)
   - com.example.myapp.credits.50 (consumable)
   - com.example.myapp.pro.monthly (auto-renewable)
   - com.example.myapp.pro.yearly (auto-renewable)

🍎 Phase 2: Syncing to App Store Connect...
   ✅ Created: 3

🐱 Phase 3: Syncing to RevenueCat (via MCP)...
   ✅ Products: 3
   ✅ Entitlements: 1 (pro)
   ✅ Offering: default

══════════════════════════════════════════════════
✅ Sync complete!
```

### RevenueCat MCP Setup

```bash
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer YOUR_V2_API_KEY"
```

---

## Command 8: `/aso-screenshots` - Screenshot Generation

### Prerequisites

- Gemini MCP installed and configured
- Simulator screenshots of your app

### Basic Usage

```
/aso-screenshots
/aso-screenshots FitFlow
```

### What It Does

**Phase 1: Spec Generation**
- Analyzes your codebase
- Generates 3-5 specs (headlines)
- Each starts with ACTION VERB
- Tells user what screenshots to capture

**Phase 2: User Provides Screenshots**
- User takes screenshots from simulator
- Matching the specs provided
- Can add more spec + screenshot pairs

**Phase 3: Gemini MCP Generation**
- Combines spec + screenshot + brand color
- Generates 3 polished versions
- User picks favorite
- Exports to App Store dimensions

### Output Structure

```
screenshots/
├── 01-track-prices/
│   ├── simulator.png      ← User's screenshot
│   ├── v1.jpg, v2.jpg, v3.jpg  ← Gemini versions
│   └── final.jpg          ← User's pick
├── final/
│   └── 01-track-prices.jpg
└── showcase.png
```

### Spec (Headline) Format

```
[ACTION VERB] + [SPECIFIC BENEFIT]

✅ Good:
- TRACK TRADING CARD PRICES
- SEARCH ANY VERSE IN SECONDS
- BUILD YOUR DREAM WORKOUT

❌ Bad:
- MANAGE YOUR STUFF (generic)
- EASY TO USE (not specific)
- BEST APP EVER (marketing fluff)
```

### Screenshot Tips (for User)

1. **Show full data** - Lists with items, not empty states
2. **Clean status bar** - 9:41 time, full battery
3. **Consistent mode** - All light or all dark
4. **Best screens** - Core features, not settings

---

## Workflows

### New App Launch

```bash
# 1. Setup credentials
/aso-setup

# 2. Full audit
/aso-audit MyNewApp

# 3. Review outputs
cat outputs/MyNewApp/00-MASTER-ACTION-PLAN.md

# 4. Generate screenshots
/aso-screenshots

# 5. Submit to stores
/aso-submit MyNewApp

# 6. Check status
/aso-status MyNewApp
```

### Quick Metadata Update

```bash
# Just update metadata
/aso MyExistingApp

# Copy to App Store Connect
# Paste metadata manually
```

### Competitor Research Only

```bash
# Research phase only
/aso-audit MyApp --research-only

# Review competitor gaps
cat outputs/MyApp/01-research/competitor-analysis.md
```

---

## Memory & Persistence

### What Gets Saved

- App name and details
- Confirmed benefits
- Keywords researched
- Generated metadata
- Screenshot pairings

### Resuming Work

The skill checks memory on every run:

```
Here's where we left off:

✅ Benefits (3 confirmed)
✅ Screenshots analyzed (5 provided)
✅ Pairings confirmed
⏳ Generation: 2 of 3 done

Ready to continue?
```

### Clearing Memory

To start fresh:
```
"Clear my ASO data for [app-name]"
```

---

## Best Practices

### Keywords

1. **Relevance first** - High volume irrelevant keywords are worthless
2. **No duplicates** - Title words NOT in keywords field
3. **Long-tail** - 3-4 word phrases for lower competition
4. **Monitor** - Update quarterly based on rankings

### Metadata

1. **Benefits over features** - "Save time" not "Uses AI"
2. **Natural language** - No keyword stuffing
3. **Clear CTA** - Tell users what to do
4. **Update regularly** - Fresh content ranks better

### Screenshots

1. **First 3 matter most** - Users rarely scroll
2. **Show core value** - Main features prominent
3. **Consistent style** - Same colors, fonts, frames
4. **Test at thumbnail** - Must be readable small

---

## Troubleshooting

### "Command not found"

```bash
# Check installation
ls ~/.claude/skills/aso/SKILL.md

# Restart Claude Code
claude --reload
```

### "Character limit exceeded"

- Skill auto-validates and warns
- Truncate intelligently (not mid-word)
- Prioritize high-value keywords

### "iTunes API failed"

- Check internet connection
- Retry after 5 seconds
- Automatic fallback to WebFetch

### "App Store Connect 401"

```bash
# Check credentials
cat ~/.aso/credentials.json

# Re-run setup
/aso-setup
```

### "Screenshot generation failed"

```bash
# Check Gemini MCP installed
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp

# Check API key set
echo $GEMINI_API_KEY
```
