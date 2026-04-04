# CLAUDE.md

This file provides guidance to Claude Code when working with this ASO skill.

## What This Is

A comprehensive **App Store Optimization (ASO) skill** for Claude Code that combines:

1. **Quick Metadata Generation** (`/aso`) - Fast listing optimization
2. **Full ASO Audit** (`/aso-audit`) - Comprehensive analysis with competitor research
3. **App Store Connect Submission** (`/aso-submit`) - Direct ASC integration
4. **Screenshot Generation** (`/aso-screenshots`) - AI-powered screenshot creation

## Architecture

```
aso-skill/
├── SKILL.md              # Main skill definition (user-invocable)
├── CLAUDE.md             # This file
├── agents/
│   ├── aso-quick.md      # Fast metadata agent (sonnet)
│   └── aso-full.md       # Full audit orchestrator (opus)
├── commands/
│   ├── aso.md            # /aso command
│   ├── aso-audit.md      # /aso-audit command
│   ├── aso-submit.md     # /aso-submit command
│   └── aso-screenshots.md # /aso-screenshots command
├── lib/
│   ├── itunes_api.py     # iTunes Search API client
│   ├── keyword_engine.py # Keyword analysis engine
│   ├── asc_api.py        # App Store Connect API client
│   └── screenshot_composer.py # Screenshot generation
└── templates/
    ├── apple-metadata.md  # Apple App Store template
    └── google-metadata.md # Google Play Store template
```

## Installation

### User-Level (All Projects)
```bash
cp -r aso-skill ~/.claude/skills/aso
```

### Project-Level
```bash
cp -r aso-skill /path/to/project/.claude/skills/aso
```

### Verification
```bash
ls ~/.claude/skills/aso/
# Should show: SKILL.md, agents/, commands/, lib/, templates/
```

## Key Design Decisions

### Multi-Source Data Strategy
1. **iTunes Search API** - Free, official, primary source
2. **WebFetch scraping** - Fallback for additional data
3. **Astro MCP** - Optional real-time rankings (if configured)
4. **User input** - Last resort for unavailable data

### Platform-Specific Limits (CRITICAL)
```yaml
apple:
  title: 30
  subtitle: 30
  promotional_text: 170
  keywords: 100
  description: 4000

google:
  title: 50
  short_description: 80
  full_description: 4000
```

### No Keyword Duplication Rule
- Words in title CANNOT appear in subtitle
- Words in title/subtitle CANNOT appear in keyword field
- Validate before every output

### Memory Persistence
The skill saves state to Claude Code memory:
- App details and preferences
- Confirmed benefits and keywords
- Screenshot pairings and assessments
- Generated metadata

This enables resuming across conversations.

## Python Modules

### itunes_api.py
```python
from lib.itunes_api import iTunesAPI

api = iTunesAPI()
apps = api.search_apps("productivity", limit=10)
analysis = api.analyze_competitors(["Todoist", "Any.do"])
```

No external dependencies. Uses urllib only.

### keyword_engine.py
```python
from lib.keyword_engine import KeywordEngine

engine = KeywordEngine()
analysis = engine.analyze_keywords(
    seed_keywords=["task manager"],
    app_features=["AI scheduling"],
    app_name="TaskFlow"
)
```

Returns prioritized keywords with placement recommendations.

### asc_api.py
```python
from lib.asc_api import ASCClient, PrivacyConfig

client = ASCClient()
if client.is_authenticated():
    config = PrivacyConfig.basic_analytics()
    # Use asc CLI for actual submission
```

Requires web session from Blitz app or `asc_web_auth` MCP tool.

### screenshot_composer.py
```python
from lib.screenshot_composer import compose_screenshot, ScreenshotConfig

config = ScreenshotConfig(
    bg_color="#E31837",
    verb="TRACK",
    desc="CARD PRICES",
    screenshot_path="simulator.png",
    output_path="output.png"
)
compose_screenshot(config)
```

Requires Pillow: `pip install Pillow`

## Command Reference

| Command | Purpose | Time |
|---------|---------|------|
| `/aso` | Quick metadata generation | 2-5 min |
| `/aso-audit` | Full ASO audit | 20-30 min |
| `/aso-submit` | ASC submission | 5-10 min |
| `/aso-screenshots` | Screenshot generation | 15-30 min |

## Workflow Patterns

### Quick Optimization
```
User: /aso TaskFlow
→ Collect app details
→ Generate metadata
→ Validate limits
→ Output copy-paste ready
→ Save to memory
```

### Full Audit
```
User: /aso-audit TaskFlow
→ Phase 1: Research (iTunes API + competitors)
→ Phase 2: Optimization (metadata generation)
→ Phase 3: Strategy (timeline + checklists)
→ Phase 4: Synthesis (master action plan)
→ Output to outputs/TaskFlow/
```

### Screenshot Generation
```
User: /aso-screenshots
→ Benefit Discovery (codebase analysis)
→ Screenshot Collection & Assessment
→ Pairing Benefits with Screenshots
→ Scaffold Generation (compose.py)
→ AI Enhancement (3 versions)
→ User Selection
→ Final Export
```

## Integration Points

### Astro MCP (Optional)
When available, use these tools:
- `list_apps` - Get user's apps
- `get_app_keywords` - Current rankings
- `search_rankings` - Track positions
- `get_keyword_suggestions` - AI suggestions

### App Store Connect
- Web session at `~/.blitz/asc-agent/web-session.json`
- Use `asc_web_auth` MCP tool to authenticate
- CLI commands: `asc web privacy plan/apply/publish`

### Gemini MCP (Screenshots)
- Required for AI screenshot enhancement
- Install: `npm install -g gemini-mcp`
- Tools: `generate_image`, `edit_image`

## Quality Standards

### Output Requirements
- All character limits validated (100% compliance)
- No keyword duplication across fields
- Copy-paste ready (no placeholders)
- Specific dates in timelines (not "Week 1")
- Actionable checklists (not vague tasks)

### Self-Assessment
Each output should score ≥ 4/5 on:
- Completeness
- Actionability
- Data Quality
- User Readiness

## Sources and Credits

This skill combines best practices from:
- [alirezarezvani/claude-code-aso-skill](https://github.com/alirezarezvani/claude-code-aso-skill) - Agent system, structured outputs
- [Mehrozsheikh/aso-appstore-listing-skill](https://github.com/Mehrozsheikh/aso-appstore-listing-skill) - Minimal skill format, Astro MCP
- [blitzdotdev/blitz-mac](https://github.com/blitzdotdev/blitz-mac) - ASC API integration
- [adamlyttleapps/claude-skill-aso-appstore-screenshots](https://github.com/adamlyttleapps/claude-skill-aso-appstore-screenshots) - Screenshot generation

## Troubleshooting

### iTunes API Timeout
→ Retry after 5 seconds
→ Fall back to WebFetch
→ Ask user for competitor data

### Character Limit Exceeded
→ Truncate intelligently (not mid-word)
→ Suggest alternative phrasing
→ Prioritize high-value keywords

### ASC Authentication Failed
→ Call `asc_web_auth` MCP tool
→ Or run: `asc web auth login --apple-id EMAIL`

### Screenshot Generation Failed
→ Check Pillow installed: `pip install Pillow`
→ Check font available: SF Pro Display Black
→ Verify simulator screenshot path exists
