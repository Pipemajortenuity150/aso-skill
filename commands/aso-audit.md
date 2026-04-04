---
name: aso-audit
description: Comprehensive ASO audit with competitor analysis, keyword research, and launch planning
---

# /aso-audit - Full ASO Audit

Execute a comprehensive App Store Optimization audit.

## Usage

```
/aso-audit [app-name]
```

## Examples

```
/aso-audit FitFlow
/aso-audit "My Fitness App"
```

## What It Does

### Phase 1: Research (10-15 min)
- Fetch competitor data via iTunes API
- Analyze top 5 competitors
- Extract keyword strategies
- Identify market gaps

### Phase 2: Optimization (5-10 min)
- Generate Apple metadata (validated)
- Generate Google metadata (validated)
- Create visual asset specifications

### Phase 3: Launch Planning (5-10 min)
- Build pre-launch checklist
- Create timeline with specific dates
- Generate review response templates

### Phase 4: Synthesis (5 min)
- Consolidate all outputs
- Create master action plan

## Output Structure

```
outputs/[app-name]/
├── 00-MASTER-ACTION-PLAN.md      # Start here
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

## Time

20-30 minutes total

## When to Use

- New app launch
- Major listing revamp
- Entering new market
- Competitive analysis needed
- Planning launch timeline

## When NOT to Use

Use `/aso` instead if you:
- Just need quick metadata
- Already have keywords
- Don't need competitor analysis

## After Completion

1. Open `outputs/[app-name]/00-MASTER-ACTION-PLAN.md`
2. Copy metadata from `02-metadata/`
3. Follow `03-launch/prelaunch-checklist.md`
4. Track `03-launch/timeline.md`

## Data Sources

- iTunes Search API (free, official)
- WebFetch scraping (fallback)
- Astro MCP (if configured)

## Related

- `/aso` - Quick metadata generation
- `/aso-submit` - Submit to App Store Connect
