# /aso-localize Command

Translate Xcode .xcstrings localization files using AI.

## Trigger
- `/aso-localize` or `/aso-localize path/to/Localizable.xcstrings`
- "translate xcstrings", "localize app", "translate to Turkish"

## Prerequisites
- Xcode 15+ project with .xcstrings file
- Claude Code (AI translation built-in)

---

## What It Does

```
📝 Localization Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Parse .xcstrings JSON
2. Extract source strings
3. AI translate to target languages
4. Write translations back
5. Validate output
```

---

## Usage

### Translate to Single Language
```
/aso-localize Localizable.xcstrings --to tr
```

### Translate to Multiple Languages
```
/aso-localize Localizable.xcstrings --to tr,de,fr,es,ja
```

### Translate All Missing
```
/aso-localize Localizable.xcstrings --all-missing
```

---

## .xcstrings Format

Xcode 15+ String Catalog format (JSON):

```json
{
  "sourceLanguage": "en",
  "strings": {
    "welcome_message": {
      "extractionState": "manual",
      "localizations": {
        "en": {
          "stringUnit": {
            "state": "translated",
            "value": "Welcome to our app!"
          }
        },
        "tr": {
          "stringUnit": {
            "state": "translated",
            "value": "Uygulamamıza hoş geldiniz!"
          }
        }
      }
    },
    "button_save": {
      "localizations": {
        "en": {
          "stringUnit": {
            "state": "translated",
            "value": "Save"
          }
        }
      }
    }
  },
  "version": "1.0"
}
```

---

## Implementation

### Parse .xcstrings

```python
import json
from pathlib import Path

def parse_xcstrings(file_path: str) -> dict:
    """Parse .xcstrings file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_source_strings(data: dict) -> dict:
    """Extract source language strings."""
    source_lang = data.get("sourceLanguage", "en")
    strings = {}

    for key, value in data.get("strings", {}).items():
        locs = value.get("localizations", {})
        if source_lang in locs:
            unit = locs[source_lang].get("stringUnit", {})
            strings[key] = unit.get("value", key)

    return strings

# Usage
data = parse_xcstrings("Localizable.xcstrings")
source = get_source_strings(data)
print(f"Found {len(source)} strings to translate")
```

### Translate with AI

```python
def translate_strings(
    strings: dict,
    target_lang: str,
    context: str = None
) -> dict:
    """
    Translate strings using Claude.

    This is done via Claude agent - agent reads strings,
    translates using its language capabilities, returns translations.
    """
    translations = {}

    # Agent translates each string
    # Context helps with domain-specific terminology
    for key, value in strings.items():
        # Claude translates naturally
        translated = translate_single(value, target_lang, context)
        translations[key] = translated

    return translations

def translate_single(text: str, target_lang: str, context: str = None) -> str:
    """
    Single string translation.

    Agent prompt:
    "Translate this UI string to {target_lang}.
     Keep it natural and concise for mobile UI.
     Context: {context}

     Original: {text}
     Translation:"
    """
    # Claude does this naturally
    pass
```

### Write Translations Back

```python
def add_translations(
    data: dict,
    translations: dict,
    target_lang: str
) -> dict:
    """Add translations to .xcstrings data."""
    for key, translated in translations.items():
        if key in data["strings"]:
            if "localizations" not in data["strings"][key]:
                data["strings"][key]["localizations"] = {}

            data["strings"][key]["localizations"][target_lang] = {
                "stringUnit": {
                    "state": "translated",
                    "value": translated
                }
            }

    return data

def save_xcstrings(data: dict, file_path: str):
    """Save .xcstrings file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## Batch Translation

```python
import json

def localize_xcstrings(
    file_path: str,
    target_langs: list,
    context: str = None
):
    """
    Full localization workflow.

    Args:
        file_path: Path to .xcstrings file
        target_langs: List of language codes ['tr', 'de', 'ja']
        context: App context for better translations
    """
    # 1. Parse
    data = parse_xcstrings(file_path)
    source = get_source_strings(data)
    print(f"📝 Found {len(source)} strings")

    # 2. Translate each language
    for lang in target_langs:
        print(f"\n🌍 Translating to {lang}...")

        # Get missing strings for this language
        missing = get_missing_strings(data, lang)
        print(f"   {len(missing)} strings to translate")

        if missing:
            # Agent translates
            translations = translate_strings(missing, lang, context)

            # Add to data
            data = add_translations(data, translations, lang)
            print(f"   ✅ {len(translations)} translated")

    # 3. Save
    save_xcstrings(data, file_path)
    print(f"\n✅ Saved to {file_path}")

def get_missing_strings(data: dict, target_lang: str) -> dict:
    """Get strings missing translation for target language."""
    source_lang = data.get("sourceLanguage", "en")
    missing = {}

    for key, value in data.get("strings", {}).items():
        locs = value.get("localizations", {})

        # Has source but not target
        if source_lang in locs and target_lang not in locs:
            unit = locs[source_lang].get("stringUnit", {})
            missing[key] = unit.get("value", key)

    return missing
```

---

## Supported Languages

```
Common App Store Languages:
─────────────────────────────────────────
en    English (source)
tr    Turkish
de    German (de-DE)
fr    French (fr-FR)
es    Spanish (es-ES)
it    Italian
pt    Portuguese (pt-BR, pt-PT)
ja    Japanese
ko    Korean
zh    Chinese (zh-Hans, zh-Hant)
nl    Dutch
ru    Russian
pl    Polish
ar    Arabic
th    Thai
vi    Vietnamese
id    Indonesian
ms    Malay
sv    Swedish
da    Danish
fi    Finnish
nb    Norwegian
```

---

## Output Example

```
/aso-localize Localizable.xcstrings --to tr,de,ja

📝 Parsing Localizable.xcstrings...
   Source: en
   Strings: 47

🌍 Translating to Turkish (tr)...
   Missing: 47 strings
   ✅ Translated: 47

🌍 Translating to German (de)...
   Missing: 47 strings
   ✅ Translated: 47

🌍 Translating to Japanese (ja)...
   Missing: 47 strings
   ✅ Translated: 47

✅ Localization complete!
   Languages: 3
   Strings: 141 total
   Saved: Localizable.xcstrings
```

---

## Translation Tips

### Provide Context
```
/aso-localize Localizable.xcstrings --to tr --context "Fitness tracking app for workouts"
```

Context helps AI choose better terminology:
- "workout" → "antrenman" (fitness) vs "egzersiz" (generic)
- "rep" → "tekrar" (fitness specific)

### Review Critical Strings
```
/aso-localize Localizable.xcstrings --to tr --review
```

Shows translations for confirmation before saving.

### Preserve Placeholders
```
Original: "Hello, %@!"
Turkish:  "Merhaba, %@!"
```

AI preserves format specifiers: `%@`, `%d`, `%s`, `{name}`, etc.

---

## Error Handling

### "File not found"
Check path is correct and file has .xcstrings extension.

### "Invalid JSON"
File may be corrupted. Try opening in Xcode first.

### "Translation failed"
Retry with smaller batch or check language code.

---

## Agent Notes

- Use native Claude translation (no external API needed)
- Batch in chunks of 20 strings to avoid rate limits
- Preserve all JSON structure and metadata
- Keep UI strings concise (mobile-friendly)
- Maintain consistent terminology across strings
- Ask user to review critical strings (buttons, errors)
