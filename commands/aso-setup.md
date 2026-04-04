# /aso-setup Command

Configure App Store Connect authentication for ASO skill.

## Trigger
- `/aso-setup`
- "configure ASC", "set up authentication", "ASC login"

## Authentication Options

### Option 1: API Key (Recommended for CI/CD)
- Create key in App Store Connect
- Download .p8 file (one-time!)
- Configure locally

### Option 2: Web Session (For iris API features)
- Login to App Store Connect in browser
- Export cookies
- Save to config

---

## Workflow

### 1. Check Current Status

```bash
mkdir -p ~/.aso

echo "=== ASO Credentials Status ==="

if [ -f ~/.aso/credentials.json ]; then
    echo "✅ API Key configured"
    cat ~/.aso/credentials.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  Key ID: {d[\"keyId\"]}')"
else
    echo "❌ No API Key"
fi

if [ -f ~/.aso/web-session.json ]; then
    echo "✅ Web session exists"
else
    echo "❌ No web session"
fi

ls ~/.aso/*.p8 2>/dev/null && echo "✅ .p8 file found" || echo "❌ No .p8 file"
```

### 2. Ask User Which Method

```
📱 App Store Connect Setup

Which authentication method?

1. API Key - For metadata, apps, IAPs (recommended)
2. Web Session - For privacy labels, special operations
3. Both - Full access
```

---

## Option 1: API Key Setup

### Step 1: Guide User to Create Key

```
📋 Create API Key in App Store Connect:

1. Go to: https://appstoreconnect.apple.com/access/integrations/api
2. Click "Generate API Key" (or "+" button)
3. Enter a name (e.g., "ASO-Skill-Key")
4. Select "Admin" access
5. Click "Generate"
6. IMPORTANT: Download the .p8 file immediately (one-time only!)
7. Note the Key ID and Issuer ID shown on page

Then provide:
- Issuer ID: (shown at top of page)
- Key ID: (shown next to key name)
- .p8 file path: (where you saved it)
```

### Step 2: Save Credentials

After user provides info:

```bash
# Move .p8 to secure location
mkdir -p ~/.aso
cp "/path/to/AuthKey_XXXX.p8" ~/.aso/
chmod 600 ~/.aso/AuthKey_*.p8

# Create credentials.json
cat > ~/.aso/credentials.json << EOF
{
  "issuerId": "USER_PROVIDED_ISSUER_ID",
  "keyId": "USER_PROVIDED_KEY_ID",
  "privateKeyPath": "~/.aso/AuthKey_KEYID.p8"
}
EOF
chmod 600 ~/.aso/credentials.json
```

### Step 3: Test Connection

```python
import jwt
import time
import json
import os
import urllib.request

# Load credentials
with open(os.path.expanduser("~/.aso/credentials.json")) as f:
    creds = json.load(f)

with open(os.path.expanduser(creds["privateKeyPath"])) as f:
    private_key = f.read()

# Generate token
now = int(time.time())
payload = {"iss": creds["issuerId"], "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"}
token = jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": creds["keyId"], "typ": "JWT"})

# Test API
req = urllib.request.Request(
    "https://api.appstoreconnect.apple.com/v1/apps?limit=1",
    headers={"Authorization": f"Bearer {token}"}
)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✅ API Key works! Found {len(data['data'])} app(s)")
except Exception as e:
    print(f"❌ API Key failed: {e}")
```

---

## Option 2: Web Session Setup

### Step 1: Guide User to Get Cookies

```
📋 Export Web Session Cookies:

1. Open: https://appstoreconnect.apple.com
2. Login with Apple ID (complete 2FA if needed)
3. Open Developer Tools (F12 or Cmd+Option+I)
4. Go to: Application → Cookies → appstoreconnect.apple.com
5. Copy these cookies:
   - myacinfo
   - dqsid
   - itctx
   - Any cookie starting with "DES"

Format as: name1=value1; name2=value2; ...
```

### Step 2: Save Session

```bash
# Create session file
cat > ~/.aso/web-session.json << 'EOF'
{
  "cookies": "USER_PROVIDED_COOKIE_STRING",
  "created": "2026-04-04T12:00:00Z"
}
EOF
chmod 600 ~/.aso/web-session.json
```

### Step 3: Test Session

```python
import json
import os
import urllib.request

with open(os.path.expanduser("~/.aso/web-session.json")) as f:
    session = json.load(f)

req = urllib.request.Request(
    "https://appstoreconnect.apple.com/iris/v1/apps?limit=1",
    headers={
        "Cookie": session["cookies"],
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✅ Web session works! Found {len(data['data'])} app(s)")
except urllib.error.HTTPError as e:
    if e.code == 401:
        print("❌ Session expired or invalid")
    else:
        print(f"❌ Error: {e.code}")
```

---

## Quick Setup Script

One-command setup for API Key:

```bash
read -p "Issuer ID: " ISSUER_ID
read -p "Key ID: " KEY_ID
read -p "Path to .p8 file: " P8_PATH

mkdir -p ~/.aso
cp "$P8_PATH" ~/.aso/
chmod 600 ~/.aso/*.p8

cat > ~/.aso/credentials.json << EOF
{
  "issuerId": "$ISSUER_ID",
  "keyId": "$KEY_ID",
  "privateKeyPath": "~/.aso/AuthKey_$KEY_ID.p8"
}
EOF

echo "✅ Credentials saved to ~/.aso/"
```

---

## Requirements

```bash
# Required for JWT generation
pip3 install PyJWT cryptography
```

---

## Troubleshooting

### "No module named 'jwt'"
```bash
pip3 install PyJWT
```

### "Invalid algorithm" error
```bash
pip3 install cryptography
```

### API Key 401 error
- Check Issuer ID (UUID format)
- Check Key ID (10 chars)
- Verify .p8 file is correct
- Key must have Admin role

### Web Session 401 error
- Cookies expired (re-login and export)
- Missing required cookies
- Try incognito window for clean session

---

## Security Notes

- .p8 files are highly sensitive - treat like passwords
- Never commit credentials to git
- Set file permissions to 600
- Web sessions expire after ~30 days
- Rotate API keys periodically
