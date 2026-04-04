# /aso - Metadata Generation & Optimization

Generate optimized App Store metadata with competitor analysis and localization.

## Usage

```bash
/aso AppName                      # Quick metadata
/aso AppName --audit              # Full audit with competitors
/aso --localize tr,de,ja          # Translate .xcstrings
```

## Modes

### Quick Mode (Default)
```bash
/aso TaskFlow
/aso "My App Name"
```

Generates copy-paste ready metadata in 2-5 minutes:
- Title (30 chars)
- Subtitle (30 chars)
- Keywords (100 chars)
- Description (4000 chars)

### Audit Mode
```bash
/aso TaskFlow --audit
/aso TaskFlow --audit --competitors "Todoist,Any.do"
```

Full ASO audit (20-30 min):
- Competitor analysis via iTunes API
- Keyword research & gaps
- Optimized metadata
- Launch checklist & timeline

Output: `outputs/[app-name]/00-MASTER-ACTION-PLAN.md`

### Localize Mode
```bash
/aso --localize tr,de,ja
/aso --localize tr --file Localizable.xcstrings
```

Translate Xcode .xcstrings files:
- AI-powered translation (70+ languages)
- Preserves placeholders (%@, %d)
- Context-aware terminology

---

## Quick Mode Output

```json
{
  "title": "TaskFlow - AI Task Manager",
  "title_chars": "28/30",
  "subtitle": "Smart Productivity & Focus",
  "subtitle_chars": "26/30",
  "keywords": "productivity,task,planner,todo,organize,schedule,reminder",
  "keywords_chars": "58/100",
  "description": "TaskFlow helps you...",
  "description_chars": "2847/4000"
}
```

---

## Audit Mode Output

```
outputs/TaskFlow/
├── 00-MASTER-ACTION-PLAN.md      # Start here
├── 01-research/
│   ├── keyword-list.md
│   ├── competitor-analysis.md
│   └── market-gaps.md
├── 02-metadata/
│   ├── apple-metadata.md
│   └── google-metadata.md
├── 03-launch/
│   ├── prelaunch-checklist.md
│   └── timeline.md
└── 04-optimization/
    └── ongoing-tasks.md
```

---

## Localize Mode

### .xcstrings Format (Xcode 15+)
```json
{
  "sourceLanguage": "en",
  "strings": {
    "welcome_message": {
      "localizations": {
        "en": {"stringUnit": {"state": "translated", "value": "Welcome!"}},
        "tr": {"stringUnit": {"state": "translated", "value": "Hoş geldiniz!"}}
      }
    }
  }
}
```

### Supported Languages
```
en, tr, de, fr, es, it, pt, ja, ko, zh-Hans, zh-Hant,
nl, ru, pl, ar, th, vi, id, ms, sv, da, fi, nb, ...
```

---

## Character Limits

| Platform | Title | Subtitle | Keywords | Description |
|----------|-------|----------|----------|-------------|
| Apple | 30 | 30 | 100 | 4000 |
| Google | 50 | - | - | 4000 |

**Rules:**
- Title words NOT in subtitle
- Title/subtitle words NOT in keywords
- No spaces after commas in keywords

---

## Examples

```bash
# Quick metadata
/aso "FitTracker - Workout Logger"

# Full audit
/aso FitTracker --audit --competitors "Strong,Hevy"

# Translate to multiple languages
/aso --localize tr,de,fr,ja --context "Fitness app"

# Localize specific file
/aso --localize tr --file Sources/Localizable.xcstrings
```
