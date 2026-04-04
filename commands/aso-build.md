# /aso-build Command

Build, archive and upload iOS apps using XcodeBuildMCP integration.

## Trigger
- `/aso-build` or `/aso-build archive`
- "build app", "archive", "upload to app store"

## Prerequisites

### XcodeBuildMCP (Required)
```bash
# Install via Homebrew
brew install getsentry/tools/xcodebuildmcp

# Or via npm
npm install -g xcodebuildmcp

# Add to Claude Code
claude mcp add xcodebuild
```

### Requirements
- macOS 14.5+
- Xcode 16.x+
- Valid code signing

---

## What It Does

```
🔨 Build Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Discover Xcode project/workspace
2. List schemes and configurations
3. Build for device/simulator
4. Archive for distribution
5. Upload to App Store Connect
```

---

## Usage

### Build for Simulator
```
/aso-build simulator
```

### Build for Device
```
/aso-build device
```

### Archive & Upload
```
/aso-build archive --upload
```

---

## XcodeBuildMCP Tools

When XcodeBuildMCP is installed, these tools become available:

| Tool | Purpose |
|------|---------|
| `discover_projects` | Find Xcode projects in directory |
| `list_schemes` | List available schemes |
| `build_for_simulator` | Build for iOS Simulator |
| `build_for_device` | Build for physical device |
| `run_on_simulator` | Run app on simulator |
| `get_logs` | Get build logs |

---

## Implementation

### Discover Projects

```
Use discover_projects tool:
"Find Xcode projects in the current directory"

Returns:
- Project/workspace paths
- Available schemes
- Configurations (Debug, Release)
```

### Build for Simulator

```
Use build_for_simulator tool:
"Build MyApp scheme for iPhone 15 Pro simulator"

Parameters:
- scheme: "MyApp"
- simulator: "iPhone 15 Pro"
- configuration: "Debug" (optional)
```

### Build for Device

```
Use build_for_device tool:
"Build MyApp for my connected iPhone"

Parameters:
- scheme: "MyApp"
- configuration: "Release"
```

### Archive

```
Use archive tool (if available):
"Archive MyApp for App Store distribution"

Parameters:
- scheme: "MyApp"
- configuration: "Release"
- export_method: "app-store"
```

---

## Full Workflow

```
/aso-build archive --upload

🔨 Build Pipeline
─────────────────────────────────────────

1. Discovering project...
   ✅ Found: MyApp.xcworkspace
   Schemes: MyApp, MyAppTests

2. Selecting scheme: MyApp
   Configuration: Release

3. Building...
   ✅ Build succeeded (2m 34s)

4. Archiving...
   ✅ Archive created: MyApp.xcarchive

5. Exporting for App Store...
   ✅ IPA created: MyApp.ipa

6. Uploading to App Store Connect...
   ✅ Upload complete!

─────────────────────────────────────────
✅ Build pipeline complete!

Next steps:
- Run /aso-version to attach build
- Run /aso-status to check readiness
- Run /aso-submit to push metadata
```

---

## Integration with ASO Workflow

```
Complete Release Workflow:

1. /aso-build archive --upload
   └── Build, archive, upload to ASC

2. /aso-version attach-build
   └── Attach uploaded build to version

3. /aso-screenshots --upload
   └── Upload App Store screenshots

4. /aso-submit
   └── Push metadata

5. /aso-status
   └── Verify everything is ready

6. /aso-version submit
   └── Submit for review
```

---

## Troubleshooting

### "XcodeBuildMCP not found"
```bash
# Install via Homebrew
brew install getsentry/tools/xcodebuildmcp

# Verify installation
xcodebuildmcp --version

# Add to Claude Code
claude mcp add xcodebuild
```

### "No provisioning profile"
- Open Xcode → Signing & Capabilities
- Enable "Automatically manage signing"
- Or manually configure profiles

### "Build failed"
```
Use get_logs tool:
"Show me the build logs"
```

Review logs for specific errors.

### "Archive export failed"
- Check code signing identity
- Verify provisioning profile matches
- Ensure certificates are valid

---

## Without XcodeBuildMCP

If XcodeBuildMCP is not available, use native xcodebuild:

```bash
# Build
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  clean build

# Archive
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -archivePath ./build/MyApp.xcarchive \
  archive

# Export
xcodebuild -exportArchive \
  -archivePath ./build/MyApp.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ExportOptions.plist

# Upload (requires Transporter or altool)
xcrun altool --upload-app \
  -f ./build/MyApp.ipa \
  -t ios \
  -u "apple_id@example.com" \
  -p "@keychain:AC_PASSWORD"
```

---

## XcodeBuildMCP Resources

- [GitHub: getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP)
- [Installation Guide](https://github.com/getsentry/XcodeBuildMCP#installation)
- [Supported IDEs](https://github.com/getsentry/XcodeBuildMCP#supported-clients)

---

## Agent Notes

- Check if XcodeBuildMCP is available first
- Fall back to native xcodebuild if needed
- Always use Release configuration for archives
- Verify code signing before building
- Keep build logs for debugging
