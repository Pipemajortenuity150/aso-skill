# /aso-release - Version & Release Management

Manage App Store versions, builds, submissions, and release notes.

## Usage

```bash
/aso-release create 1.0.0         # Create new version
/aso-release attach               # Attach latest build
/aso-release submit               # Submit for review
/aso-release notes                # Generate What's New
/aso-release phased [action]      # Phased release control
```

## Subcommands

### create - New Version
```bash
/aso-release create 1.0.0
/aso-release create 2.0 --app MyApp
```

Creates new App Store version in PREPARE_FOR_SUBMISSION state.

### attach - Attach Build
```bash
/aso-release attach               # Latest valid build
/aso-release attach --build-id ID # Specific build
```

Lists available builds and attaches to current version.

### submit - Submit for Review
```bash
/aso-release submit
/aso-release submit --expedite    # Request expedited review
```

Runs pre-submission checks, then submits for App Review.

### notes - What's New
```bash
/aso-release notes                # From git commits
/aso-release notes --changelog    # From CHANGELOG.md
/aso-release notes --to tr,de     # With translation
```

Generates user-friendly release notes from git history.

### phased - Phased Release
```bash
/aso-release phased start         # Enable phased release
/aso-release phased pause         # Pause at current %
/aso-release phased resume        # Resume rollout
/aso-release phased complete      # Release to 100%
```

---

## Version States

| State | Description |
|-------|-------------|
| `PREPARE_FOR_SUBMISSION` | Editable |
| `WAITING_FOR_REVIEW` | Submitted |
| `IN_REVIEW` | Being reviewed |
| `PENDING_DEVELOPER_RELEASE` | Approved, manual release |
| `READY_FOR_SALE` | Live |
| `REJECTED` | Rejected |

---

## Phased Release Schedule

| Day | Percentage |
|-----|------------|
| 1 | 1% |
| 2 | 2% |
| 3 | 5% |
| 4 | 10% |
| 5 | 20% |
| 6 | 50% |
| 7 | 100% |

---

## What's New Generation

### From Git
```bash
/aso-release notes --since v1.0.0
```

Reads commits since tag, generates user-friendly notes:

```
🚀 New Features
• Track prices across multiple marketplaces
• Dark mode support

🔧 Improvements
• Faster search results
• Better image quality

🐛 Bug Fixes
• Fixed crash on offline mode
```

### Templates

**Major Release:**
```
🎉 Version 2.0 is here!

✨ New Design
• Fresh, modern interface

🚀 New Features
• [Feature 1]
• [Feature 2]

Thank you for your support! ❤️
```

**Bug Fix:**
```
Bug Fixes
• Fixed [issue]
• Stability improvements

Thanks for your patience!
```

---

## Implementation

```python
from lib.asc_api import ASCClient, generate_token

token = generate_token()
client = ASCClient(token)

# Get app
apps = client.list_apps()
app_id = apps[0]["id"]

# Create version
result = client.create_version(app_id, "1.0.0")
version_id = result["data"]["id"]

# Attach build
builds = client.list_builds(app_id)
valid = next(b for b in builds if b["attributes"]["processingState"] == "VALID")
client.attach_build_to_version(version_id, valid["id"])

# Submit for review
client.submit_for_review(version_id)

# Enable phased release
client.create_phased_release(version_id)
```

---

## Pre-Submission Checklist

Before `/aso-release submit`:

- [ ] Build attached (VALID state)
- [ ] Description filled (all locales)
- [ ] Keywords filled (all locales)
- [ ] Screenshots uploaded
- [ ] Privacy Policy URL live
- [ ] Support URL live
- [ ] Age rating configured

Run `/aso-connect status` to verify all items.

---

## Examples

```bash
# Full release workflow
/aso-release create 1.2.0
/aso-release attach
/aso-release notes --to tr,de
/aso-release submit
/aso-release phased start
```
