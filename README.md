# 🚀 ASO Skill - Complete App Store Optimization for Claude Code

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Open Source](https://img.shields.io/badge/Open_Source-100%25-brightgreen.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-purple.svg)
![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20Android-orange.svg)
[![GitHub stars](https://img.shields.io/github/stars/furkancingoz/aso-skill?style=social)](https://github.com/furkancingoz/aso-skill)

**100% Open Source ASO toolkit for Claude Code**

*No subscriptions. No API keys required. No hidden costs.*

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Commands](#-commands) • [Workflows](#-workflows)

</div>

---

## 📋 Overview

**ASO Skill** is a **completely free and open source** App Store Optimization toolkit for Claude Code. Generate metadata, analyze competitors, create screenshots, manage versions, and submit to App Store Connect - all with 6 simple commands.

### 🆓 Why Open Source?

- **No monthly fees** - Unlike AppTweak, Sensor Tower, or ASOTools
- **No API limits** - Use as much as you want
- **Full transparency** - See exactly how it works
- **Community driven** - Contribute and improve together
- **Self-hosted** - Your data stays with you

### 🎯 What Makes This Different

| Feature | Traditional ASO Tools | ASO Skill |
|---------|----------------------|-----------|
| **Price** | $50-500/month | **Free forever** |
| Metadata Generation | Manual writing | AI-powered, character-validated |
| Competitor Analysis | Expensive subscriptions | Free iTunes API integration |
| Screenshots | Design software needed | AI-generated with Gemini MCP |
| App Store Connect | Manual submission | Direct API integration |
| Version Management | ASC web interface | CLI commands |
| Workflow | Fragmented tools | 6 unified commands |

---

## ✨ Features

### 📝 Metadata Optimization (`/aso`)
- **Quick mode** - Copy-paste ready metadata in minutes
- **Audit mode** - Full competitor analysis and research
- **Localize mode** - Translate .xcstrings to 70+ languages
- **Character validation** - All limits enforced

### 🔌 App Store Connect (`/aso-connect`)
- **Setup wizard** - Configure API credentials
- **Status check** - Verify submission readiness
- **Sync metadata** - Push to ASC directly

### 🚀 Release Management (`/aso-release`)
- **Create versions** - New App Store versions
- **Attach builds** - Link builds to versions
- **Submit for review** - One command submission
- **What's New** - Generate from git commits
- **Phased release** - Control rollout percentage

### 📸 Assets (`/aso-assets`)
- **Screenshots** - AI-generated with Gemini MCP
- **IAP setup** - Create and manage in-app purchases
- **Upload** - Push assets to ASC

### 💬 Management (`/aso-manage`)
- **Reviews** - AI response suggestions
- **Legal docs** - Privacy Policy, Terms, EULA
- **GDPR/CCPA** - Compliance ready

### 🔨 Build (`/aso-build`)
- **XcodeBuildMCP** - Build, archive, upload
- **Simulator/Device** - Target any platform
- **TestFlight** - Direct upload

---

## 📦 Installation

### Option 1: User-Level (Recommended)

```bash
git clone https://github.com/furkancingoz/aso-skill.git ~/.claude/skills/aso
```

### Option 2: Project-Level

```bash
mkdir -p .claude/skills
git clone https://github.com/furkancingoz/aso-skill.git .claude/skills/aso
```

### Dependencies

```bash
# Required: JWT token generation
pip3 install PyJWT cryptography

# Optional: Screenshot generation
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp
export GEMINI_API_KEY="your_key"

# Optional: IAP sync with RevenueCat
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp \
  --header "Authorization: Bearer YOUR_V2_API_KEY"
```

---

## 🚀 Quick Start

### 1. Setup Credentials
```
/aso-connect setup
```

### 2. Generate Metadata
```
/aso TaskFlow
```

### 3. Create Screenshots
```
/aso-assets screenshots
```

### 4. Submit to App Store
```
/aso-release create 1.0.0
/aso-release attach
/aso-connect sync
/aso-release submit
```

---

## 🎮 Commands

| Command | Purpose | Subcommands |
|---------|---------|-------------|
| `/aso` | Metadata generation | (default), --audit, --localize |
| `/aso-connect` | ASC integration | setup, status, sync |
| `/aso-release` | Version management | create, attach, submit, notes, phased |
| `/aso-assets` | Screenshots & IAP | screenshots, iap |
| `/aso-manage` | Reviews & legal | reviews, legal |
| `/aso-build` | Xcode build | (default), --archive, --upload |

### Command Examples

```bash
# Quick metadata
/aso "My App Name"

# Full audit with competitors
/aso MyApp --audit --competitors "Todoist,Any.do"

# Translate to multiple languages
/aso --localize tr,de,ja

# Check submission readiness
/aso-connect status

# Create new version and submit
/aso-release create 1.2.0
/aso-release attach
/aso-release submit

# Generate screenshots
/aso-assets screenshots

# Manage reviews
/aso-manage reviews --negative

# Generate legal documents
/aso-manage legal privacy
```

---

## 📊 Workflows

### Full App Store Submission

```
/aso-connect setup                # 1. Configure credentials
/aso AppName --audit              # 2. Research + optimize
/aso-assets screenshots           # 3. Generate screenshots
/aso-assets iap                   # 4. Set up IAPs
/aso-release create 1.0.0         # 5. Create version
/aso-release attach               # 6. Attach build
/aso-connect sync                 # 7. Push metadata
/aso-connect status               # 8. Verify readiness
/aso-release submit               # 9. Submit for review
```

### Version Update

```
/aso-release notes                # Generate What's New from git
/aso-release create 1.1.0         # Create new version
/aso-release attach               # Attach latest build
/aso-release submit               # Submit for review
/aso-release phased start         # Enable phased release
```

### Localization

```
/aso --localize tr,de,ja          # Translate .xcstrings
/aso-connect sync --locale tr     # Sync Turkish metadata
```

---

## 🔧 Character Limits

### Apple App Store

| Field | Limit | Notes |
|-------|-------|-------|
| Title | 30 | Include primary keyword |
| Subtitle | 30 | No overlap with title |
| Keywords | 100 | Comma-separated, no spaces |
| Promo Text | 170 | Editable without update |
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
├── agents/
│   ├── aso-quick.md      # Fast metadata (sonnet)
│   └── aso-full.md       # Full audit (opus)
├── commands/
│   ├── aso.md            # Metadata + audit + localize
│   ├── aso-connect.md    # Setup + status + sync
│   ├── aso-release.md    # Version + build + submit
│   ├── aso-assets.md     # Screenshots + IAP
│   ├── aso-manage.md     # Reviews + legal
│   └── aso-build.md      # Xcode build
├── lib/
│   ├── itunes_api.py     # iTunes Search API
│   ├── keyword_engine.py # Keyword analysis
│   └── asc_api.py        # App Store Connect API
└── templates/
    ├── apple-metadata.md
    └── google-metadata.md
```

---

## 🔌 Integrations

### App Store Connect API (Built-in)
- Direct API integration
- JWT authentication
- Version, build, metadata management

### iTunes Search API (Built-in)
- Free, official Apple API
- Competitor analysis
- No authentication required

### Gemini MCP (Screenshots)
```bash
claude mcp add gemini-mcp -s user -- npx -y @houtini/gemini-mcp
export GEMINI_API_KEY="your_key"
```

### RevenueCat MCP (IAP Sync)
```bash
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp \
  --header "Authorization: Bearer YOUR_V2_API_KEY"
```

### XcodeBuildMCP (Build)
- Build, archive, upload
- See: https://github.com/getsentry/XcodeBuildMCP

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

### How does App Store Connect work?
Direct API calls using JWT authentication. Run `/aso-connect setup` to configure.

### Can I customize the agents?
**Yes.** All agents are Markdown files - edit freely.

---

## 🤝 Contributing

Contributions welcome!

```bash
git clone https://github.com/YOUR_USERNAME/aso-skill.git
git checkout -b feature/your-feature
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## ⭐ Star History

<a href="https://star-history.com/#furkancingoz/aso-skill&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=furkancingoz/aso-skill&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=furkancingoz/aso-skill&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=furkancingoz/aso-skill&type=Date" />
 </picture>
</a>

---

<div align="center">

**Created by [@furkancingoz](https://github.com/furkancingoz)**

[⬆ Back to Top](#-aso-skill---complete-app-store-optimization-for-claude-code)

</div>
