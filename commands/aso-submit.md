---
name: aso-submit
description: Submit app to App Store Connect - configure privacy labels, apply metadata, initiate submission
---

# /aso-submit - App Store Connect Submission

Direct integration with App Store Connect for submission.

## Usage

```
/aso-submit [app-name]
/aso-submit [app-name] --app-id [ASC_APP_ID]
```

## Examples

```
/aso-submit FitFlow
/aso-submit FitFlow --app-id 1234567890
```

## Prerequisites

1. **Web Session**: Authenticated App Store Connect session
   - Cached at `~/.blitz/asc-agent/web-session.json`
   - Or call `asc_web_auth` MCP tool to authenticate

2. **App ID**: Your App Store Connect app ID
   - Find in App Store Connect URL
   - Or provide with `--app-id` flag

3. **Metadata Ready**: Generated via `/aso` or `/aso-audit`

## What It Does

### Step 1: Authentication Check
```bash
test -f ~/.blitz/asc-agent/web-session.json && echo "OK" || echo "NEED_AUTH"
```

If not authenticated → Call `asc_web_auth` MCP tool

### Step 2: Privacy Nutrition Labels

Configures App Store privacy declarations:

```yaml
options:
  - No data collected
  - Data collected (specify types)
    - Contact info (name, email, phone)
    - Location (precise, coarse)
    - Identifiers (user ID, device ID)
    - Usage data (product interaction)
    - Diagnostics (crash data, performance)
```

Commands:
```bash
# Preview changes
asc web privacy plan --app APP_ID --file /tmp/privacy.json --pretty

# Apply changes
asc web privacy apply --app APP_ID --file /tmp/privacy.json --allow-deletes --confirm

# Publish (make live)
asc web privacy publish --app APP_ID --confirm
```

### Step 3: Metadata Application

Applies optimized metadata to App Store Connect:
- App name
- Subtitle
- Keywords
- Description
- Promotional text
- What's New

### Step 4: Verification

```bash
# Verify privacy labels
asc web privacy pull --app APP_ID --pretty

# Verify metadata
asc web metadata pull --app APP_ID --locale en-US
```

## Privacy Declaration Examples

### No Data Collected
```json
{
  "schemaVersion": 1,
  "dataUsages": []
}
```

### Basic Analytics Only
```json
{
  "schemaVersion": 1,
  "dataUsages": [
    {
      "category": "CRASH_DATA",
      "purposes": ["ANALYTICS"],
      "dataProtections": ["DATA_NOT_LINKED_TO_YOU"]
    }
  ]
}
```

### User Accounts + Analytics
```json
{
  "schemaVersion": 1,
  "dataUsages": [
    {
      "category": "NAME",
      "purposes": ["APP_FUNCTIONALITY"],
      "dataProtections": ["DATA_LINKED_TO_YOU"]
    },
    {
      "category": "EMAIL_ADDRESS",
      "purposes": ["APP_FUNCTIONALITY"],
      "dataProtections": ["DATA_LINKED_TO_YOU"]
    },
    {
      "category": "CRASH_DATA",
      "purposes": ["ANALYTICS"],
      "dataProtections": ["DATA_NOT_LINKED_TO_YOU"]
    }
  ]
}
```

## Time

5-10 minutes

## Workflow

```
/aso-submit FitFlow

1. ✓ Checking authentication...
2. ✓ Session valid

3. 📋 Privacy Labels Configuration
   Does your app collect user data?
   > Yes / No

   [If Yes] What types?
   > [ ] Name, Email
   > [ ] Location
   > [ ] Analytics/Crash data
   > [ ] Other

4. ⏳ Applying privacy labels...
5. ✓ Privacy labels published

6. 📝 Applying metadata...
   - Title: "FitFlow - AI Fitness Coach"
   - Subtitle: "Personalized Workouts"
   - Keywords: (95/100 chars)

7. ✓ Metadata applied

8. 📋 Submission Readiness
   - [ ] App binary uploaded
   - [✓] Privacy labels complete
   - [✓] Metadata complete
   - [ ] Screenshots uploaded

Ready to submit? (y/n)
```

## Error Handling

### 401 Not Authorized
```
Session expired. Running authentication...
→ Call asc_web_auth MCP tool
→ Open Apple ID login in Blitz
→ Retry after authentication
```

### 409 Conflict
```
App may already exist or conflict detected.
→ Check App Store Connect for existing app
→ Verify bundle ID is unique
```

## Security

- **NEVER** log or print session cookies
- Session cached securely in keychain
- Authentication handled via web session, not API keys

## Related

- `/aso` - Generate metadata
- `/aso-audit` - Full ASO audit

## Requirements

- Blitz app installed (for MCP tools)
- App Store Connect account
- App already created in ASC (or use `asc-app-create` skill)
