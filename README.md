# 🚀 ASO Skill - Complete App Store Optimization for Claude Code

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-purple.svg)
![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20Android-orange.svg)

**The most comprehensive ASO toolkit for Claude Code**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Commands](#-commands) • [Screenshots](#-screenshot-generation)

</div>

---

## 📋 Overview

**ASO Skill** is a complete App Store Optimization toolkit that combines the best features from 4 leading ASO projects into one unified skill for Claude Code. Generate metadata, analyze competitors, create screenshots, and submit to App Store Connect - all from natural language commands.

### 🎯 What Makes This Different

| Feature | Traditional ASO Tools | ASO Skill |
|---------|----------------------|-----------|
| Metadata Generation | Manual writing | AI-powered, character-validated |
| Competitor Analysis | Expensive subscriptions | Free iTunes API integration |
| Screenshots | Design software needed | AI-generated with device frames |
| App Store Connect | Manual submission | Direct API integration |
| Workflow | Fragmented tools | Unified commands |

---

## ✨ Features

### 📝 Metadata Optimization
- **Copy-paste ready** - Character limits validated
- **No duplication** - Automatic keyword conflict detection
- **Both platforms** - Apple App Store + Google Play Store
- **Natural language** - No keyword stuffing

### 🔍 Competitor Intelligence
- **iTunes Search API** - Free, official Apple data
- **Keyword extraction** - From competitor titles/descriptions
- **Gap analysis** - Find opportunities competitors miss
- **Best practices** - Learn from top apps

### 📸 Screenshot Generation
- **Benefit discovery** - AI analyzes your codebase
- **Device frames** - Professional iPhone mockups
- **AI enhancement** - Nano Banana Pro / Gemini MCP
- **App Store ready** - Exact pixel dimensions

### 🚀 App Store Connect
- **Privacy labels** - Automated configuration
- **Metadata submission** - Direct API integration
- **Web session auth** - Secure authentication

---

## 📦 Installation

### Option 1: User-Level Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/furkancingoz/aso-skill.git
cd aso-skill

# Install to Claude Code skills directory
cp -r . ~/.claude/skills/aso/

# Verify installation
ls ~/.claude/skills/aso/
```

### Option 2: Project-Level Installation

```bash
# From your project directory
mkdir -p .claude/skills
cp -r /path/to/aso-skill .claude/skills/aso/
```

### Option 3: Direct Clone

```bash
git clone https://github.com/furkancingoz/aso-skill.git ~/.claude/skills/aso
```

### Dependencies (Optional)

```bash
# For screenshot generation
pip install Pillow

# For AI screenshot enhancement
npm install -g @houtini/gemini-mcp
```

### Font Requirement (Screenshots)

For screenshot generation, install **SF Pro Display Black**:
- Download from [Apple Developer Fonts](https://developer.apple.com/fonts/)
- Install to `/Library/Fonts/SF-Pro-Display-Black.otf`

---

## 🚀 Quick Start

### 1. Quick Metadata Generation

```
/aso TaskFlow - AI task manager for professionals
```

**Output:** Copy-paste ready metadata in 2-5 minutes

### 2. Full ASO Audit

```
/aso-audit TaskFlow
```

**Output:** Complete research, metadata, and launch plan in 20-30 minutes

### 3. Screenshot Creation

```
/aso-screenshots
```

**Output:** Professional App Store screenshots with device frames

---

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `/aso [app-name]` | Quick metadata generation (any language) |
| `/aso-audit [app-name]` | Full ASO audit with competitor analysis |
| `/aso-submit [app-name]` | Push to App Store Connect (metadata, privacy, screenshots) |
| `/aso-iap [app-name]` | Set up IAPs & Subscriptions |
| `/aso-screenshots` | Generate App Store screenshot specifications |
| `/aso-setup` | Configure credentials (API key, web session) |

---

## 📊 Output Structure

### Quick Mode (`/aso`)
```
Copy-paste ready JSON:
{
  "title": "TaskFlow - AI Task Manager",
  "subtitle": "Smart Productivity & Focus",
  "keywords": "productivity,organize,planner...",
  "description": "..."
}
```

### Audit Mode (`/aso-audit`)
```
outputs/[app-name]/
├── 00-MASTER-ACTION-PLAN.md      # Start here
├── 01-research/
│   ├── keyword-list.md           # Prioritized keywords
│   ├── competitor-analysis.md    # Gap analysis
│   └── market-gaps.md            # Opportunities
├── 02-metadata/
│   ├── apple-metadata.md         # Copy-paste for ASC
│   ├── google-metadata.md        # Copy-paste for Play Console
│   └── visual-assets-spec.md     # Screenshot specs
├── 03-launch/
│   ├── prelaunch-checklist.md    # 47-item validation
│   └── timeline.md               # Specific dates
└── 04-optimization/
    ├── review-templates.md       # Response templates
    └── ongoing-tasks.md          # Daily/weekly tasks
```

### Screenshot Mode (`/aso-screenshots`)
```
screenshots/
├── 01-track-prices/
│   ├── scaffold.png              # Layout template
│   ├── v1.jpg, v2.jpg, v3.jpg    # AI versions
│   └── v1-resized.jpg            # App Store ready
├── final/
│   ├── 01-track-prices.jpg       # Approved
│   └── 02-search-cards.jpg
└── showcase.png                   # Preview image
```

---

## 📱 Screenshot Generation

### How It Works

1. **Benefit Discovery** - AI analyzes your codebase for core features
2. **Screenshot Collection** - Assess and rate simulator screenshots
3. **Pairing** - Match benefits with best screenshots
4. **Scaffold** - Generate deterministic layout with compose.py
5. **Enhancement** - AI adds polish and breakout elements
6. **Export** - Crop to exact App Store dimensions

### Supported Sizes

| Display | Dimensions |
|---------|------------|
| iPhone 6.5" | 1242 × 2688 px |
| iPhone 6.7" | 1290 × 2796 px (default) |
| iPhone 6.9" | 1320 × 2868 px |

### Benefit Headline Format

```
[ACTION VERB] + [BENEFIT]

Examples:
✅ TRACK TRADING CARD PRICES
✅ SEARCH ANY VERSE IN SECONDS
✅ BUILD YOUR DREAM WORKOUT

❌ MANAGE YOUR STUFF (too generic)
❌ USE OUR APP (not benefit-focused)
```

---

## 🔧 Character Limits

### Apple App Store

| Field | Limit | Notes |
|-------|-------|-------|
| Title | 30 | Include primary keyword |
| Subtitle | 30 | No overlap with title |
| Promo Text | 170 | Editable without update |
| Keywords | 100 | Comma-separated, no spaces |
| Description | 4000 | Include app name 3-5x |

### Google Play Store

| Field | Limit | Notes |
|-------|-------|-------|
| Title | 50 | More keywords allowed |
| Short Desc | 80 | Shows in search results |
| Full Desc | 4000 | Keywords ARE indexed |

---

## 🛠️ Architecture

```
aso-skill/
├── SKILL.md              # Main skill definition
├── CLAUDE.md             # Development guidance
├── README.md             # This file
├── INSTALL.md            # Detailed installation
├── LICENSE               # MIT License
├── agents/
│   ├── aso-quick.md      # Fast metadata (sonnet)
│   └── aso-full.md       # Full audit (opus)
├── commands/
│   ├── aso.md            # /aso
│   ├── aso-audit.md      # /aso-audit
│   ├── aso-submit.md     # /aso-submit
│   └── aso-screenshots.md # /aso-screenshots
├── lib/
│   ├── itunes_api.py     # iTunes Search API
│   ├── keyword_engine.py # Keyword analysis
│   ├── asc_api.py        # App Store Connect
│   └── screenshot_composer.py # Screenshot gen
└── templates/
    ├── apple-metadata.md
    └── google-metadata.md
```

---

## 🔌 Integrations

### iTunes Search API (Built-in)
- Free, official Apple API
- No authentication required
- Competitor metadata and ratings

### Astro MCP (Optional)
- Real-time keyword rankings
- App ratings history
- Setup: https://tryastro.app/docs/mcp/

### Gemini MCP (Optional)
- AI screenshot enhancement
- Install: `npm install -g @houtini/gemini-mcp`

### App Store Connect (Direct API)
- Direct submission via ASC API
- Privacy labels configuration
- JWT authentication (API Key)

---

## 📚 Credits

This skill combines best practices from:

| Project | Contribution |
|---------|--------------|
| [alirezarezvani/claude-code-aso-skill](https://github.com/alirezarezvani/claude-code-aso-skill) | Multi-agent system, structured outputs |
| [Mehrozsheikh/aso-appstore-listing-skill](https://github.com/Mehrozsheikh/aso-appstore-listing-skill) | Minimal skill format, Astro MCP |
| [adamlyttleapps/claude-skill-aso-appstore-screenshots](https://github.com/adamlyttleapps/claude-skill-aso-appstore-screenshots) | Screenshot generation |

---

## ❓ FAQ

### Do I need paid ASO tools?
**No.** This skill uses free iTunes Search API and industry benchmarks.

### Can I use this for both iOS and Android?
**Yes.** Generates metadata for Apple App Store and Google Play Store.

### How accurate are keyword volumes?
Estimates based on industry benchmarks (±20%). Use Apple Search Ads for exact volumes.

### How does App Store Connect integration work?
Direct API calls using JWT authentication. Run `/aso-setup` to configure your API key, then use `/aso-submit` to push metadata.

### Can I customize the agents?
**Yes.** All agents are Markdown files - edit freely.

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Additional data sources** - AppTweak, Sensor Tower integration
2. **Localization** - Multi-language metadata
3. **Analytics** - Keyword ranking tracking
4. **Documentation** - Video tutorials

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/aso-skill.git

# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git commit -m "feat: add your feature"

# Push and create PR
git push origin feature/your-feature
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Documentation:** [INSTALL.md](INSTALL.md), [CLAUDE.md](CLAUDE.md)
- **Issues:** Open an issue on GitHub
- **Templates:** Check `templates/` folder

---

<div align="center">

**Created by [@furkancingoz](https://github.com/furkancingoz)**

[⬆ Back to Top](#-aso-skill---complete-app-store-optimization-for-claude-code)

</div>
