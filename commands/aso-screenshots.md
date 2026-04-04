# /aso-screenshots - App Store Screenshot Generator

Create professional, high-converting App Store screenshots.

## Usage

```
/aso-screenshots [app-name]
```

## What It Does

```
📸 Screenshot Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: Benefit Discovery
└── Analyze codebase for core features
└── Generate 3-5 ACTION VERB headlines
└── User confirms/refines

Phase 2: Screenshot Pairing
└── Collect simulator screenshots
└── Rate: Great / Usable / Retake
└── Pair with benefits

Phase 3: Scaffold Generation (compose.py)
└── Pillow-based deterministic layout
└── Text + Device frame + Screenshot
└── Output: scaffold.png

Phase 4: AI Enhancement (Gemini MCP)
└── Generate 3 polished versions
└── User picks favorite
└── Crop to App Store dimensions
```

## Prerequisites

### 1. Python + Pillow
```bash
pip3 install Pillow
```

### 2. SF Pro Display Font
Download from [Apple Developer Fonts](https://developer.apple.com/fonts/) and install to `/Library/Fonts/`

### 3. Gemini MCP (for AI enhancement)
```bash
# Install Gemini MCP
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp

# Set API key (get from https://aistudio.google.com/apikey)
export GEMINI_API_KEY="your_api_key_here"
```

---

## Phase 1: Benefit Discovery

Analyze the app's codebase and identify compelling benefits:

```
Good Headlines:
✅ TRACK TRADING CARD PRICES
✅ SEARCH ANY VERSE IN SECONDS
✅ BUILD YOUR DREAM WORKOUT

Bad Headlines:
❌ MANAGE YOUR COLLECTION (too generic)
❌ SEARCH EASILY (not specific)
❌ GET FIT (boring)
```

Format: `[ACTION VERB] + [SPECIFIC BENEFIT]`

---

## Phase 2: Screenshot Collection

### Requirements
- Full data states (not empty)
- Clean status bar (9:41, full battery)
- Consistent mode (all light or all dark)
- Core features (not settings)

### Assessment
- **Great** → Use as-is
- **Usable** → Can work with it
- **Retake** → Coach for better shot

---

## Phase 3: Scaffold Generation

Use `screenshot_composer.py`:

```bash
python3 lib/screenshot_composer.py \
    --bg "#E31837" \
    --verb "TRACK" \
    --desc "TRADING CARD PRICES" \
    --screenshot path/to/simulator.png \
    --output screenshots/01-track/scaffold.png
```

### Output
- Solid background color
- Centered headline text
- Device frame with screenshot
- Pixel-perfect layout

---

## Phase 4: AI Enhancement (Gemini MCP)

### Using Gemini MCP Tools

**Generate enhanced version:**
```
Use generate_image tool:

"Create an App Store screenshot with:
- Bold red (#E31837) background
- White text 'TRACK' large at top
- 'TRADING CARD PRICES' below
- iPhone 15 Pro frame with this app screenshot
- Professional polish, slight 3D depth
- Breakout UI elements floating beside device
- 1290x2796 pixels"
```

**Edit existing scaffold:**
```
Use edit_image tool on scaffold.png:

"Enhance this App Store screenshot:
- Add subtle gradient to background
- Make device frame more photorealistic
- Add floating UI card elements
- Professional App Store quality"
```

### Generate 3 Versions
```
For each benefit:
1. v1.jpg - Clean, minimal
2. v2.jpg - With breakout elements
3. v3.jpg - Bold, dynamic
```

---

## Crop & Resize

After AI generation, crop to exact App Store dimensions:

```python
from lib.screenshot_composer import crop_to_app_store_dimensions

crop_to_app_store_dimensions(
    "screenshots/01-track/v1.jpg",
    "screenshots/01-track/v1-final.jpg",
    target_w=1290,
    target_h=2796
)
```

---

## App Store Connect Dimensions

| Display | Portrait | Landscape |
|---------|----------|-----------|
| iPhone 6.5" | 1242 x 2688px | 2688 x 1242px |
| iPhone 6.7" | 1290 x 2796px | 2796 x 1290px |
| iPhone 6.9" | 1320 x 2868px | 2868 x 1320px |

**Default: iPhone 6.7" (1290 x 2796px)**

---

## Output Structure

```
screenshots/
├── 01-track-prices/
│   ├── scaffold.png        ← compose.py output
│   ├── v1.jpg, v2.jpg, v3.jpg  ← Gemini versions
│   └── v1-final.jpg        ← Cropped to ASC size
├── 02-search-cards/
│   └── ...
├── final/
│   ├── 01-track-prices.jpg
│   ├── 02-search-cards.jpg
│   └── ...
└── showcase.png            ← Side-by-side preview
```

---

## Workflow States

Progress saved to memory:
- ✅ Benefits confirmed
- ✅ Screenshots analyzed
- ✅ Pairings confirmed
- ✅ Brand color selected
- ⏳ Generation in progress

Resume anytime with `/aso-screenshots`

---

## Full Example

```bash
# 1. Generate scaffold
python3 lib/screenshot_composer.py \
    --bg "#E31837" \
    --verb "TRACK" \
    --desc "TRADING CARD PRICES" \
    --screenshot ~/Desktop/sim1.png \
    --output screenshots/01/scaffold.png

# 2. Enhance with Gemini (in Claude)
"Use generate_image to create 3 App Store screenshot versions based on scaffold.png"

# 3. User picks v2

# 4. Crop to final size
python3 -c "
from lib.screenshot_composer import crop_to_app_store_dimensions
crop_to_app_store_dimensions('screenshots/01/v2.jpg', 'screenshots/final/01.jpg')
"
```

---

## Gemini MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `generate_image` | Create new image from prompt |
| `edit_image` | Modify existing image |

**Tips:**
- Be specific about dimensions (1290x2796)
- Mention "App Store screenshot" for style
- Request "iPhone 15 Pro frame"
- Ask for "breakout elements" for dynamic look

---

## Sources

- [Gemini MCP Setup](https://houtini.com/how-to-make-images-with-claude-and-gemini-mcp/)
- [Nano Banana MCP](https://github.com/YCSE/nanobanana-mcp)
- [Google AI Studio](https://aistudio.google.com/apikey)
