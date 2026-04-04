# /aso-setup Command

Configure App Store Connect credentials and authentication.

## Trigger
- `/aso-setup`
- "configure ASC", "set up App Store Connect", "create API key"

## Workflow

### 1. Check Current Status

```bash
echo "=== Blitz Installation ==="
ls ~/.blitz/ 2>/dev/null || echo "Blitz not installed"

echo "=== Web Session ==="
test -f ~/.blitz/asc-agent/web-session.json && echo "✅ Session exists" || echo "❌ No session"

echo "=== API Keys ==="
ls ~/.blitz/AuthKey_*.p8 2>/dev/null || echo "No API keys"

echo "=== ASC CLI ==="
~/.blitz/bin/asc auth status 2>/dev/null || echo "Not authenticated"
```

### 2. Options Menu

Present options:
1. **Web Session Login** - For web-based operations (metadata, privacy labels)
2. **Create API Key** - For CLI/CI/CD operations
3. **Check Status** - Show current auth state

### 3a. Web Session Login

```bash
# Option 1: Via MCP tool
Call asc_web_auth MCP tool

# Option 2: Via CLI
asc web auth login --apple-id "user@email.com"
```

This opens Apple ID login in Blitz, handles 2FA, and saves session.

### 3b. Create API Key

**Step 1: Ask for key name**
```
What would you like to name this API key?
(e.g., "Claude-Code-Key", "CI-CD-Key")
```

**Step 2: Create key via iris API**

```python
import json, urllib.request, base64, os, time

KEY_NAME = "USER_PROVIDED_NAME"

# Read session
session_path = os.path.expanduser('~/.blitz/asc-agent/web-session.json')
with open(session_path) as f:
    store = json.loads(f.read())

session = store['sessions'][store['last_key']]
cookie_str = '; '.join(
    f'{c["name"]}={c["value"]}'
    for cl in session['cookies'].values() for c in cl
    if c.get('name') and c.get('value')
)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://appstoreconnect.apple.com',
    'Referer': 'https://appstoreconnect.apple.com/',
    'Cookie': cookie_str
}

# Create key
create_body = json.dumps({
    'data': {
        'type': 'apiKeys',
        'attributes': {
            'nickname': KEY_NAME,
            'roles': ['ADMIN'],
            'allAppsVisible': True,
            'keyType': 'PUBLIC_API'
        }
    }
}).encode()

req = urllib.request.Request(
    'https://appstoreconnect.apple.com/iris/v1/apiKeys',
    data=create_body, method='POST', headers=headers)
resp = urllib.request.urlopen(req)
create_data = json.loads(resp.read().decode())

key_id = create_data['data']['id']

# Download private key (ONE TIME ONLY!)
time.sleep(0.5)
req = urllib.request.Request(
    f'https://appstoreconnect.apple.com/iris/v1/apiKeys/{key_id}?fields%5BapiKeys%5D=privateKey',
    method='GET', headers=headers)
resp = urllib.request.urlopen(req)
dl_data = json.loads(resp.read().decode())

pk_b64 = dl_data['data']['attributes']['privateKey']
private_key_pem = base64.b64decode(pk_b64).decode()

# Get issuer ID
time.sleep(0.35)
req = urllib.request.Request(
    f'https://appstoreconnect.apple.com/iris/v1/apiKeys/{key_id}?include=provider',
    method='GET', headers=headers)
resp = urllib.request.urlopen(req)
provider_data = json.loads(resp.read().decode())
issuer_id = provider_data['data']['relationships']['provider']['data']['id']

# Save .p8 file
p8_path = os.path.expanduser(f'~/.blitz/AuthKey_{key_id}.p8')
with open(p8_path, 'w') as f:
    f.write(private_key_pem)
os.chmod(p8_path, 0o600)

print(f'Key ID: {key_id}')
print(f'Issuer ID: {issuer_id}')
print(f'Private Key: {p8_path}')
```

**Step 3: Configure CLI**
```bash
asc auth login --key-id KEY_ID --issuer-id ISSUER_ID --private-key-path ~/.blitz/AuthKey_KEY_ID.p8
```

**Step 4: Pre-fill Blitz form**
```
Call asc_set_credentials MCP tool with:
- issuerId: ISSUER_ID
- keyId: KEY_ID
- privateKeyPath: ~/.blitz/AuthKey_KEY_ID.p8
```

### 4. Verify Setup

```bash
asc auth status
asc apps list | head -5
```

## Requirements

| Operation | Requires |
|-----------|----------|
| Web Session | Blitz installed, Apple ID |
| API Key | Web Session + Admin role |
| CLI Auth | API Key (.p8 file) |

## Common Issues

### "No web session found"
→ Run `/aso-setup` and choose "Web Session Login"

### "Session expired" (401)
→ Re-authenticate: `asc web auth login`

### "Cannot create key - not Admin"
→ User needs Account Holder or Admin role in ASC

### "Private key already downloaded"
→ p8 can only be downloaded once. Create a new key.

## Agent Notes

- Always ask for key name, never use defaults
- NEVER print session cookies
- Warn user that .p8 is one-time download
- Save .p8 with 0600 permissions
- Call `asc_set_credentials` after key creation
