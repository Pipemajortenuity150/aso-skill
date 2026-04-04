# /aso-whatsnew Command

Generate "What's New" release notes from git commits or changelog.

## Trigger
- `/aso-whatsnew` or `/aso-whatsnew 1.2.0`
- "generate release notes", "what's new", "changelog"

## Prerequisites
- Git repository with commit history
- Or CHANGELOG.md file

---

## What It Does

```
📝 What's New Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Collect changes (git log or CHANGELOG)
2. AI summarize for users
3. Translate to target languages
4. Push to App Store Connect
```

---

## Usage

### From Git Commits
```
/aso-whatsnew --from-git

# Since last tag
/aso-whatsnew --since v1.1.0

# Last N commits
/aso-whatsnew --commits 20
```

### From CHANGELOG
```
/aso-whatsnew --from-changelog

# Specific version
/aso-whatsnew --version 1.2.0
```

### With Translation
```
/aso-whatsnew --to tr,de,ja
```

---

## Implementation

### Collect from Git

```python
import subprocess

def get_commits_since_tag(tag: str = None) -> list:
    """Get commits since last tag or specific tag."""
    if tag:
        cmd = f"git log {tag}..HEAD --pretty=format:'%s'"
    else:
        # Get last tag
        last_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            text=True
        ).strip()
        cmd = f"git log {last_tag}..HEAD --pretty=format:'%s'"

    result = subprocess.check_output(cmd, shell=True, text=True)
    return [line.strip() for line in result.split('\n') if line.strip()]

def categorize_commits(commits: list) -> dict:
    """Categorize commits by type."""
    categories = {
        "features": [],
        "fixes": [],
        "improvements": [],
        "other": []
    }

    for commit in commits:
        lower = commit.lower()
        if any(k in lower for k in ["feat", "add", "new"]):
            categories["features"].append(commit)
        elif any(k in lower for k in ["fix", "bug", "patch"]):
            categories["fixes"].append(commit)
        elif any(k in lower for k in ["improve", "update", "enhance", "refactor"]):
            categories["improvements"].append(commit)
        else:
            categories["other"].append(commit)

    return categories
```

### Generate User-Friendly Notes

```python
def generate_whatsnew(commits: list, context: str = None) -> str:
    """
    AI generates user-friendly release notes.

    Agent prompt:
    "Convert these developer commits into user-friendly release notes.
     - Focus on user benefits, not technical details
     - Keep it concise (under 4000 chars)
     - Use friendly, conversational tone
     - Group similar changes

     Commits:
     {commits}

     App context: {context}
    "
    """
    # Claude generates naturally
    pass

# Example output:
"""
What's New in 1.2.0

🚀 New Features
• Track prices across multiple marketplaces
• Dark mode support

🔧 Improvements
• Faster search results
• Better card image quality

🐛 Bug Fixes
• Fixed crash when adding cards offline
• Resolved sync issues with collection
"""
```

### Push to ASC

```python
from lib.asc_api import ASCClient, generate_token

def push_whatsnew(app_id: str, whatsnew_text: str, locales: list = None):
    """Push What's New to App Store Connect."""
    token = generate_token()
    client = ASCClient(token)

    # Get editable version
    version = client.get_editable_version(app_id)
    if not version:
        raise Exception("No editable version found")

    version_id = version["id"]

    # Get localizations
    locs = client.get_version_localizations(version_id)

    for loc in locs:
        locale = loc["attributes"]["locale"]

        # Skip if not in target locales
        if locales and locale not in locales:
            continue

        # Translate if needed
        text = whatsnew_text
        if locale != "en" and locale not in ["en-GB", "en-US", "en-AU"]:
            text = translate_whatsnew(whatsnew_text, locale)

        # Update
        client.update_localization(loc["id"], {
            "whatsNew": text
        })
        print(f"✅ Updated {locale}")
```

---

## Output Example

```
/aso-whatsnew --from-git --to tr,de

📝 Generating What's New...

Git commits since v1.1.0: 15
─────────────────────────────────────────

Features (3):
  • feat: add price tracking
  • feat: implement dark mode
  • feat: add widget support

Fixes (5):
  • fix: crash on offline add
  • fix: sync issues
  ...

Improvements (7):
  • improve: search performance
  ...

Generated Release Notes:
─────────────────────────────────────────

🚀 New Features
• Track prices across multiple marketplaces
• Dark mode - easier on your eyes at night
• Home screen widget for quick access

🔧 Improvements
• Search is now 2x faster
• Card images load in higher quality
• Better offline support

🐛 Bug Fixes
• Fixed crash when adding cards offline
• Resolved sync issues with your collection
• Minor stability improvements

Characters: 487/4000 ✅

🌍 Translating...
  ✅ Turkish (tr)
  ✅ German (de)

📤 Pushing to App Store Connect...
  ✅ en-GB
  ✅ tr
  ✅ de-DE

✅ What's New updated for 3 locales!
```

---

## Character Limit

**What's New field: 4000 characters**

Keep it concise - users scan, don't read. Aim for 300-500 characters.

---

## Best Practices

### DO
- Focus on user benefits
- Use bullet points
- Group related changes
- Mention major new features first
- Thank users for feedback

### DON'T
- List technical details
- Include commit hashes
- Mention internal refactoring
- Write walls of text
- Use developer jargon

---

## Templates

### Major Release
```
🎉 Version 2.0 is here!

We've completely redesigned the app based on your feedback:

✨ New Design
• Fresh, modern interface
• Easier navigation

🚀 New Features
• [Feature 1]
• [Feature 2]

Thank you for your continued support! ❤️
```

### Minor Update
```
What's New in 1.2.0

• [Main improvement]
• [Bug fix 1]
• [Bug fix 2]

Thanks for using [App Name]!
```

### Bug Fix Release
```
Bug Fixes

• Fixed [issue 1]
• Fixed [issue 2]
• Stability improvements

We appreciate your patience and feedback!
```

---

## Agent Notes

- Read git log or CHANGELOG first
- Focus on user-facing changes
- Keep under 500 characters for readability
- Always translate for multi-language apps
- Preview before pushing to ASC
