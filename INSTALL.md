# Installation Guide

Complete installation instructions for ASO Skill.

---

## Quick Install (2 minutes)

```bash
# Clone and install
git clone https://github.com/furkancingoz/aso-skill.git ~/.claude/skills/aso

# Verify
ls ~/.claude/skills/aso/SKILL.md
```

**Done!** Start using with `/aso MyApp`

---

## Detailed Installation

### Prerequisites

| Requirement | Version | Required For |
|-------------|---------|--------------|
| Claude Code | Latest | All features |
| Python 3 | 3.8+ | API calls, screenshots |
| PyJWT | Latest | App Store Connect API |
| Pillow | Latest | Screenshot generation |
| Node.js | 18+ | Gemini MCP (optional) |

### Step 1: Clone Repository

**Option A: User-Level (Recommended)**
```bash
git clone https://github.com/furkancingoz/aso-skill.git ~/.claude/skills/aso
```

**Option B: Project-Level**
```bash
mkdir -p .claude/skills
git clone https://github.com/furkancingoz/aso-skill.git .claude/skills/aso
```

**Option C: Manual Download**
1. Download ZIP from GitHub
2. Extract to `~/.claude/skills/aso/`

### Step 2: Install Python Dependencies

```bash
# Required for App Store Connect API
pip3 install PyJWT cryptography

# Optional for screenshot generation
pip3 install Pillow
```

### Step 3: Verify Installation

```bash
# Check files exist
ls ~/.claude/skills/aso/

# Expected output:
# SKILL.md  CLAUDE.md  README.md  agents/  commands/  lib/  templates/
```

### Step 4: Test in Claude Code

```bash
# Start Claude Code
claude

# Test quick command
/aso TestApp - a test application
```

---

## App Store Connect Setup

For direct App Store Connect integration (`/aso-submit`, `/aso-status`):

### Step 1: Create API Key

1. Go to: https://appstoreconnect.apple.com/access/integrations/api
2. Click "Generate API Key"
3. Select "Admin" role
4. Download .p8 file (ONE TIME ONLY!)
5. Note the Issuer ID and Key ID

### Step 2: Configure Credentials

```bash
# Create credentials directory
mkdir -p ~/.aso

# Move .p8 file
mv ~/Downloads/AuthKey_XXXXX.p8 ~/.aso/
chmod 600 ~/.aso/AuthKey_*.p8

# Create credentials file
cat > ~/.aso/credentials.json << 'EOF'
{
  "issuerId": "YOUR_ISSUER_ID",
  "keyId": "YOUR_KEY_ID",
  "privateKeyPath": "~/.aso/AuthKey_YOUR_KEY_ID.p8"
}
EOF
chmod 600 ~/.aso/credentials.json
```

### Step 3: Test API Connection

```bash
cd ~/.claude/skills/aso
python3 lib/asc_api.py
```

Expected output:
```
Testing ASC API Client...
--------------------------------------------------

1. Checking credentials...
   API Key: ✅
   Web Session: ❌

2. Testing JWT generation...
   ✅ Token generated (XXX chars)

3. Testing API connection...
   ✅ Connected! Found X app(s)
```

---

## Optional Dependencies

### Screenshot Generation

For `/aso-screenshots` command:

```bash
# Install Pillow
pip3 install Pillow
```

**Font Requirement:**
- Download SF Pro Display Black from [Apple Developer](https://developer.apple.com/fonts/)
- Install to `/Library/Fonts/SF-Pro-Display-Black.otf`

### Gemini MCP (AI Screenshot Enhancement)

```bash
# Install Gemini MCP server
npm install -g @houtini/gemini-mcp
```

Configure in `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "gemini": {
      "command": "gemini-mcp"
    }
  }
}
```

### Astro MCP (Real-time Rankings)

For real-time App Store rankings and ratings:

1. Sign up at [tryastro.app](https://tryastro.app/?aff=kdX8mz)
2. Follow setup at [tryastro.app/docs/mcp](https://tryastro.app/docs/mcp/)

---

## Installation Verification

### Test Each Feature

```bash
# 1. Quick metadata
/aso TestApp

# 2. Full audit (creates outputs/ folder)
/aso-audit TestApp

# 3. Test Python modules
cd ~/.claude/skills/aso
python3 lib/itunes_api.py
python3 lib/asc_api.py
```

### Expected iTunes API Output

```
Testing iTunes Search API...
--------------------------------------------------

1. Searching for 'productivity' apps:
   - Todoist: 4.8★ (120655 ratings)
   - Any.do: 4.6★ (49604 ratings)
   ...

2. Analyzing competitors:
   - Found 3 competitors
   - Average rating: 4.7★
   ...

--------------------------------------------------
iTunes API test complete!
```

---

## Troubleshooting

### Command Not Found

**Symptom:** `/aso` doesn't work

**Fix:**
1. Check skill location: `ls ~/.claude/skills/aso/SKILL.md`
2. Restart Claude Code: `claude --reload`
3. Verify SKILL.md has correct frontmatter

### iTunes API Timeout

**Symptom:** Competitor fetch fails

**Fix:**
1. Check internet connection
2. Retry after 5 seconds
3. Use WebFetch fallback (automatic)

### PyJWT Not Found

**Symptom:** App Store Connect API fails

**Fix:**
```bash
pip3 install PyJWT cryptography
```

### Pillow Not Found

**Symptom:** Screenshot generation fails

**Fix:**
```bash
pip3 install Pillow
```

### Font Not Found

**Symptom:** compose.py fails with font error

**Fix:**
1. Download SF Pro from Apple Developer
2. Install to `/Library/Fonts/`
3. Or modify font path in `lib/screenshot_composer.py`

### App Store Connect Auth Failed

**Symptom:** `/aso-submit` returns 401

**Fix:**
1. Check `~/.aso/credentials.json` exists
2. Verify Issuer ID and Key ID are correct
3. Ensure .p8 file path is correct
4. Regenerate API key if needed

---

## Updating

### Pull Latest Changes

```bash
cd ~/.claude/skills/aso
git pull origin main
```

### Reinstall from Scratch

```bash
rm -rf ~/.claude/skills/aso
git clone https://github.com/furkancingoz/aso-skill.git ~/.claude/skills/aso
```

---

## Uninstalling

```bash
rm -rf ~/.claude/skills/aso
rm -rf ~/.aso  # Remove credentials (optional)
```

---

## Directory Structure

After installation:

```
~/.claude/skills/aso/
├── SKILL.md              # Main skill (required)
├── CLAUDE.md             # Developer guidance
├── README.md             # Documentation
├── INSTALL.md            # This file
├── LICENSE               # MIT License
├── agents/
│   ├── aso-quick.md      # Fast metadata agent
│   ├── aso-full.md       # Full audit agent
│   └── asc-api.md        # ASC API agent
├── commands/
│   ├── aso.md            # /aso command
│   ├── aso-audit.md      # /aso-audit command
│   ├── aso-submit.md     # /aso-submit command
│   ├── aso-iap.md        # /aso-iap command
│   ├── aso-setup.md      # /aso-setup command
│   ├── aso-status.md     # /aso-status command
│   └── aso-screenshots.md # /aso-screenshots command
├── lib/
│   ├── itunes_api.py     # iTunes API client
│   ├── keyword_engine.py # Keyword analysis
│   ├── asc_api.py        # App Store Connect API
│   └── screenshot_composer.py
└── templates/
    ├── apple-metadata.md
    └── google-metadata.md
```

---

## Next Steps

1. **Read:** [README.md](README.md) for features overview
2. **Setup:** Run `/aso-setup` to configure App Store Connect
3. **Try:** `/aso YourApp` to generate metadata
4. **Explore:** `/aso-audit YourApp` for full analysis
5. **Customize:** Edit agents in `agents/` folder
