# /aso-screenshots - App Store Screenshot Generator

Create professional, high-converting App Store screenshots with Gemini MCP.

## Usage

```
/aso-screenshots [app-name]
```

## What It Does

```
📸 Screenshot Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: Spec Generation (Headlines)
└── Analyze codebase for core features
└── Generate 3-5 ACTION VERB headlines (= SPECS)
└── User confirms/refines specs

Phase 2: User Captures Screenshots
└── Give specs to user
└── User takes screenshots from simulator matching specs
└── User can add more spec + screenshot pairs

Phase 3: Gemini MCP Generation
└── Combine: Spec + Screenshot + Brand color
└── Generate 3 polished versions per spec
└── User picks favorite
└── Export to App Store dimensions
```

## Prerequisites

### Gemini MCP (Required)
```bash
# Install Gemini MCP
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp

# Set API key (get from https://aistudio.google.com/apikey)
export GEMINI_API_KEY="your_api_key_here"
```

---

## Phase 1: Spec Generation (Headlines)

Analyze the app's codebase and generate compelling specs:

```
Good Specs (Headlines):
✅ TRACK TRADING CARD PRICES
✅ SEARCH ANY VERSE IN SECONDS
✅ BUILD YOUR DREAM WORKOUT

Bad Specs:
❌ MANAGE YOUR COLLECTION (too generic)
❌ SEARCH EASILY (not specific)
❌ GET FIT (boring)
```

Format: `[ACTION VERB] + [SPECIFIC BENEFIT]`

### Output to User
```
📋 Screenshot Specs:

1. "TRACK TRADING CARD PRICES"
   → Take screenshot of: Price tracking screen with cards

2. "SEARCH ANY VERSE IN SECONDS"
   → Take screenshot of: Search results screen

3. "BUILD YOUR DREAM WORKOUT"
   → Take screenshot of: Workout builder screen

Tips:
- Full data states (not empty)
- Clean status bar (9:41, full battery)
- Consistent mode (all light or all dark)
```

---

## Phase 2: User Provides Screenshots

User takes screenshots from simulator matching specs:

```
User: Here's my screenshot for "TRACK TRADING CARD PRICES"
      [simulator_screenshot.png]

Agent: Got it! Want to add another spec + screenshot?

User: Yes, add "COMPARE PRICES INSTANTLY"
      [compare_screenshot.png]
```

---

## Phase 3: Gemini MCP Generation

For each spec + screenshot pair, generate App Store screenshot:

### Prompt Template
```
Use generate_image tool with user's screenshot:

"Create an App Store screenshot:
- Spec/Headline: [SPEC FROM PHASE 1]
- Brand color: [USER'S BRAND COLOR]
- Screenshot: [USER'S SIMULATOR SCREENSHOT]
- iPhone 15 Pro device frame
- Bold headline text at top
- Professional App Store quality
- 1290x2796 pixels (iPhone 6.7")"
```

### Example Prompt
```
"Create an App Store screenshot with:
- Bold red (#E31837) background
- White text 'TRACK' large at top
- 'TRADING CARD PRICES' below
- iPhone 15 Pro frame containing this app screenshot
- Professional polish, slight 3D depth
- Optional: Breakout UI elements floating beside device
- 1290x2796 pixels"
```

### Generate 3 Versions per Spec
```
For each spec + screenshot:
1. v1 - Clean, minimal
2. v2 - With breakout elements
3. v3 - Bold, dynamic

User picks favorite → Final export
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
│   ├── simulator.png       ← User's screenshot
│   ├── v1.jpg, v2.jpg, v3.jpg  ← Gemini versions
│   └── final.jpg           ← User's pick
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
- ✅ Specs (headlines) generated
- ✅ Brand color selected
- ✅ Screenshots received from user
- ⏳ Generation in progress

Resume anytime with `/aso-screenshots`

---

## Full Example

```
1. Agent analyzes codebase → generates specs:
   - "TRACK TRADING CARD PRICES"
   - "SEARCH ANY CARD INSTANTLY"
   - "BUILD YOUR COLLECTION"

2. User takes screenshots from simulator matching each spec

3. User provides: screenshot + brand color (#E31837)

4. Agent uses Gemini MCP:
   "Create App Store screenshot with:
   - Red (#E31837) background
   - 'TRACK TRADING CARD PRICES' headline
   - iPhone 15 Pro frame with this screenshot
   - 1290x2796 pixels"

5. Gemini generates 3 versions → User picks favorite

6. Repeat for remaining specs
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
