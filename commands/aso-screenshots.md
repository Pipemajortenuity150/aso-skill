---
name: aso-screenshots
description: Generate high-converting App Store screenshots with AI-powered design and device frames
---

# /aso-screenshots - App Store Screenshot Generator

Create professional, high-converting App Store screenshots.

## Usage

```
/aso-screenshots [app-name]
```

## Examples

```
/aso-screenshots
/aso-screenshots FitFlow
```

## What It Does

### Phase 1: Benefit Discovery
- Analyze codebase for core features
- Identify 3-5 compelling benefit headlines
- Each benefit starts with ACTION VERB
- User confirms/refines benefits

### Phase 2: Screenshot Collection & Pairing
- Collect simulator screenshots from user
- Assess each screenshot (Great/Usable/Retake)
- Coach on retakes if needed
- Pair screenshots with benefits

### Phase 3: Generation
- Create scaffold with compose.py (deterministic layout)
- Enhance with AI (Nano Banana Pro / Gemini)
- Generate 3 versions per benefit
- User picks best version
- Crop/resize to exact App Store dimensions

## Output

```
screenshots/
├── 01-track-prices/
│   ├── scaffold.png
│   ├── v1.jpg, v2.jpg, v3.jpg
│   └── v1-resized.jpg, v2-resized.jpg, v3-resized.jpg
├── 02-search-cards/
│   └── ...
├── final/
│   ├── 01-track-prices.jpg
│   ├── 02-search-cards.jpg
│   └── ...
└── showcase.png
```

## App Store Connect Dimensions

| Display | Portrait | Landscape |
|---------|----------|-----------|
| iPhone 6.5" | 1242 x 2688px | 2688 x 1242px |
| iPhone 6.7" | 1290 x 2796px | 2796 x 1290px |
| iPhone 6.9" | 1320 x 2868px | 2868 x 1320px |

Default: iPhone 6.7" (1290 x 2796px)

## Screenshot Format

Each screenshot includes:
- **Line 1**: ACTION VERB (largest, boldest text)
- **Line 2**: Benefit descriptor (smaller, still bold)
- **Device frame**: iPhone mockup with app screenshot
- **Background**: Bold brand color
- **Breakout elements**: Optional UI panels popping out

## Benefit Headline Examples

Good:
- "TRACK TRADING CARD PRICES"
- "SEARCH ANY VERSE IN SECONDS"
- "BUILD YOUR DREAM WORKOUT"

Bad (too generic):
- "MANAGE YOUR COLLECTION"
- "SEARCH EASILY"
- "GET FIT"

## Prerequisites

For AI enhancement:
- Gemini MCP server (`npm install -g gemini-mcp`)
- Or manual enhancement workflow

For scaffold generation:
- Python 3 with Pillow (`pip install Pillow`)
- SF Pro Display Black font

## Workflow States

The skill saves progress to memory:
- ✅ Benefits confirmed
- ✅ Screenshots analyzed
- ✅ Pairings confirmed
- ✅ Brand color selected
- ⏳ Generation in progress

Resume anytime with `/aso-screenshots`

## Tips

1. **Screenshots should be at their best** - full data, not empty states
2. **Clean status bar** - 9:41 time, full battery, full signal
3. **Consistent mode** - all light or all dark mode
4. **Rich content** - lists with items, charts with data
5. **No settings screens** - show core features

## Time

- Benefit Discovery: 10-15 min
- Screenshot Pairing: 5-10 min
- Generation: 5-10 min per screenshot

## Related

- `/aso` - Quick metadata generation
- `/aso-audit` - Full ASO audit
- `/aso-submit` - Submit to App Store Connect
