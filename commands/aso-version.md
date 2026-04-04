# /aso-version Command

Manage App Store Connect versions - create, list, attach builds, and submit for review.

## Trigger
- `/aso-version` or `/aso-version AppName`
- "create version", "new version", "attach build", "submit for review"

## Prerequisites
- API Key configured (`~/.aso/credentials.json`)
- App exists in App Store Connect

---

## Quick Actions

### List Versions
```
/aso-version list
```

### Create New Version
```
/aso-version create 1.0.0
/aso-version create 2.0 --app MyApp
```

### Attach Build
```
/aso-version attach-build
/aso-version attach-build --build-id BUILD_ID
```

### Submit for Review
```
/aso-version submit
```

---

## Implementation

### List All Versions

```python
from lib.asc_api import ASCClient, generate_token

token = generate_token()
client = ASCClient(token)

# Get app
apps = client.list_apps()
app_id = apps[0]["id"]  # or filter by name

# List versions
versions = client.get_app_versions(app_id)
for v in versions:
    attrs = v["attributes"]
    print(f'{attrs["versionString"]} - {attrs["appStoreState"]}')
```

### Create New Version

```python
# Create version 1.0.0
result = client.create_version(app_id, "1.0.0")
version_id = result["data"]["id"]
print(f"Created version: {version_id}")
```

### Get Editable Version

```python
# Get version in PREPARE_FOR_SUBMISSION state
version = client.get_editable_version(app_id)
if version:
    print(f'Editable: {version["attributes"]["versionString"]}')
else:
    print("No editable version - create one first")
```

### List Available Builds

```python
builds = client.list_builds(app_id, limit=5)
for b in builds:
    attrs = b["attributes"]
    print(f'{b["id"]}: v{attrs["version"]} ({attrs["processingState"]})')
```

### Attach Build to Version

```python
# Get latest build
builds = client.list_builds(app_id, limit=1)
if builds:
    build_id = builds[0]["id"]

    # Get editable version
    version = client.get_editable_version(app_id)
    if version:
        client.attach_build_to_version(version["id"], build_id)
        print(f"Attached build {build_id} to version")
```

### Submit for Review

```python
version = client.get_editable_version(app_id)
if version:
    # Pre-check: Run /aso-status first!
    result = client.submit_for_review(version["id"])
    print("Submitted for review!")
```

---

## Version States

| State | Description |
|-------|-------------|
| `PREPARE_FOR_SUBMISSION` | Editable, can modify |
| `WAITING_FOR_REVIEW` | Submitted, waiting |
| `IN_REVIEW` | Being reviewed |
| `PENDING_DEVELOPER_RELEASE` | Approved, manual release |
| `READY_FOR_SALE` | Live on App Store |
| `REJECTED` | Review rejected |

---

## Workflow Example

```python
from lib.asc_api import ASCClient, generate_token

token = generate_token()
client = ASCClient(token)

# 1. Get app
apps = client.list_apps()
app = next(a for a in apps if "MyApp" in a["attributes"]["name"])
app_id = app["id"]
print(f"App: {app['attributes']['name']} ({app_id})")

# 2. Check for editable version or create one
version = client.get_editable_version(app_id)
if not version:
    print("Creating new version 1.0.0...")
    result = client.create_version(app_id, "1.0.0")
    version = result["data"]

version_id = version["id"]
print(f"Version: {version['attributes']['versionString']} ({version_id})")

# 3. List and attach build
builds = client.list_builds(app_id)
if builds:
    # Find VALID build
    valid_build = next(
        (b for b in builds if b["attributes"]["processingState"] == "VALID"),
        None
    )
    if valid_build:
        client.attach_build_to_version(version_id, valid_build["id"])
        print(f"Attached build: {valid_build['attributes']['version']}")
    else:
        print("No valid build found - upload via Xcode first")
else:
    print("No builds found")

# 4. (Optional) Enable phased release
# client.create_phased_release(version_id)

# 5. Submit for review (after /aso-status passes)
# client.submit_for_review(version_id)
```

---

## Output Example

```
📱 Version Management - MyApp

App: MyApp - Smart Photo Editor (1234567890)

Versions:
─────────────────────────────────────────────
  1.0.0  READY_FOR_SALE         Released 2026-01-15
  1.1.0  PREPARE_FOR_SUBMISSION Current

Available Builds:
─────────────────────────────────────────────
  ✅ 1.1.0 (42) - VALID - Uploaded 2026-04-04
  ✅ 1.1.0 (41) - VALID - Uploaded 2026-04-03
  ⏳ 1.1.0 (43) - PROCESSING

Actions:
  [1] Attach build 42 to version 1.1.0
  [2] Create new version
  [3] Submit for review
```

---

## Error Handling

### "No editable version"
Create a new version first:
```python
client.create_version(app_id, "1.0.0")
```

### "Build not valid"
Build is still processing. Wait and retry:
```python
build = client.get_build(build_id)
print(build["attributes"]["processingState"])  # PROCESSING, VALID, INVALID
```

### "Version already exists"
A version with this number already exists. Use a different number.

### 409 Conflict
Another version is already in review. Wait for it to complete or cancel it.

---

## Agent Notes

- Always check `/aso-status` before submitting
- Only VALID builds can be attached
- One version can be in review at a time
- Phased release is optional but recommended for major updates
