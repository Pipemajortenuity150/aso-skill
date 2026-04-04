# Usage Guide

Complete guide to using ASO Skill for App Store Optimization.

---

## Quick Reference

| Command | Use Case | Time |
|---------|----------|------|
| `/aso` | Quick metadata | 2-5 min |
| `/aso-audit` | Full analysis | 20-30 min |
| `/aso-submit` | ASC submission | 5-10 min |
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

- Blitz app installed and running
- Authenticated with Apple ID
- App already created in ASC

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
2. ✓ Session valid

3. 📋 Privacy Labels
   Does your app collect data? [Yes/No]

4. ⏳ Applying privacy labels...
5. ✓ Labels published

6. 📝 Applying metadata...
7. ✓ Metadata applied

Ready to submit!
```

---

## Command 4: `/aso-screenshots` - Screenshot Generation

### Prerequisites

- Python 3 with Pillow
- SF Pro Display Black font
- Gemini MCP (optional, for AI enhancement)
- Simulator screenshots of your app

### Basic Usage

```
/aso-screenshots
/aso-screenshots FitFlow
```

### What It Does

**Phase 1: Benefit Discovery**
- Analyzes your codebase
- Identifies 3-5 core benefits
- Each starts with ACTION VERB

**Phase 2: Screenshot Pairing**
- Collects simulator screenshots
- Rates: Great / Usable / Retake
- Pairs benefits with screenshots

**Phase 3: Generation**
- Creates scaffold (deterministic)
- AI enhancement (3 versions)
- User picks favorite
- Crops to App Store dimensions

### Output Structure

```
screenshots/
├── 01-track-prices/
│   ├── scaffold.png
│   ├── v1.jpg, v2.jpg, v3.jpg
│   └── v1-resized.jpg
├── final/
│   └── 01-track-prices.jpg
└── showcase.png
```

### Benefit Headline Format

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

### Screenshot Tips

1. **Show full data** - Lists with items, not empty states
2. **Clean status bar** - 9:41 time, full battery
3. **Consistent mode** - All light or all dark
4. **Best screens** - Core features, not settings

---

## Workflows

### New App Launch

```bash
# 1. Full audit
/aso-audit MyNewApp

# 2. Review outputs
cat outputs/MyNewApp/00-MASTER-ACTION-PLAN.md

# 3. Generate screenshots
/aso-screenshots

# 4. Submit to stores
/aso-submit MyNewApp
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

### "Screenshot generation failed"

```bash
# Check Pillow
pip3 install Pillow

# Check font
ls /Library/Fonts/SF-Pro-Display-Black.otf
```
