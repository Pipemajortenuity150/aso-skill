# /aso-sync Command

Sync IAP/Subscription configuration between Project, App Store Connect, and RevenueCat.

## Trigger
- `/aso-sync` or `/aso-sync AppName`
- "sync IAPs", "sync subscriptions", "sync products"

## What It Does

```
📂 Project Code          🍎 App Store Connect       🐱 RevenueCat MCP
─────────────────        ────────────────────       ─────────────────
StoreKit Config    →     IAP Products         →     Products
Products.swift     →     Subscriptions        →     Entitlements
Pricing            →     Price Schedule       →     Offerings
```

## Prerequisites

### 1. App Store Connect API Key
```bash
# Already configured via /aso-setup
cat ~/.aso/credentials.json
```

### 2. RevenueCat MCP Server
```bash
# Install RevenueCat MCP (one-time)
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer YOUR_API_V2_SECRET_KEY"
```

Get V2 API key from: https://app.revenuecat.com → Project → API Keys

---

## Phase 1: Project Scan

Scan project for IAP definitions:

```python
import os, json, re

def scan_project_iaps(project_path):
    """Find IAP definitions in project."""
    iaps = []

    # 1. Check StoreKit Configuration file (.storekit)
    for root, dirs, files in os.walk(project_path):
        for f in files:
            if f.endswith('.storekit'):
                path = os.path.join(root, f)
                with open(path) as file:
                    config = json.load(file)
                    for product in config.get('products', []):
                        iaps.append({
                            'id': product['id'],
                            'type': product['type'],
                            'displayName': product.get('displayName', ''),
                            'price': product.get('price', 0),
                            'source': 'storekit'
                        })

    # 2. Check Swift files for product IDs
    product_pattern = r'["\']([a-z0-9_.]+\.(subscription|credits|pro|premium|lifetime|monthly|yearly|weekly)[a-z0-9_.]*)["\']'
    for root, dirs, files in os.walk(project_path):
        for f in files:
            if f.endswith('.swift'):
                path = os.path.join(root, f)
                with open(path) as file:
                    content = file.read()
                    matches = re.findall(product_pattern, content, re.IGNORECASE)
                    for match in matches:
                        product_id = match[0]
                        if not any(p['id'] == product_id for p in iaps):
                            iaps.append({
                                'id': product_id,
                                'type': guess_type(product_id),
                                'source': 'swift'
                            })

    return iaps

def guess_type(product_id):
    """Guess product type from ID."""
    pid = product_id.lower()
    if any(x in pid for x in ['monthly', 'yearly', 'weekly', 'annual']):
        return 'auto-renewable'
    elif 'lifetime' in pid:
        return 'non-consumable'
    elif 'credits' in pid:
        return 'consumable'
    return 'subscription'
```

---

## Phase 2: App Store Connect Sync

Create/update IAPs in ASC:

```python
import jwt, time, json, os, urllib.request

def generate_token():
    with open(os.path.expanduser("~/.aso/credentials.json")) as f:
        creds = json.load(f)
    with open(os.path.expanduser(creds["privateKeyPath"])) as f:
        pk = f.read()
    return jwt.encode(
        {"iss": creds["issuerId"], "iat": int(time.time()), "exp": int(time.time())+1200, "aud": "appstoreconnect-v1"},
        pk, algorithm="ES256", headers={"kid": creds["keyId"], "typ": "JWT"}
    )

def asc_api(method, endpoint, token, data=None):
    url = f"https://api.appstoreconnect.apple.com/v1/{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def sync_to_asc(app_id, iaps, token):
    """Sync IAPs to App Store Connect."""
    existing = asc_api("GET", f"apps/{app_id}/inAppPurchasesV2", token)
    existing_ids = {p["attributes"]["productId"] for p in existing["data"]}

    results = {"created": [], "skipped": [], "errors": []}

    for iap in iaps:
        if iap['id'] in existing_ids:
            results['skipped'].append(iap['id'])
            continue

        iap_type_map = {
            'consumable': 'CONSUMABLE',
            'non-consumable': 'NON_CONSUMABLE',
            'auto-renewable': 'AUTO_RENEWABLE_SUBSCRIPTION'
        }
        asc_type = iap_type_map.get(iap.get('type', '').lower(), 'CONSUMABLE')

        try:
            data = {
                "data": {
                    "type": "inAppPurchases",
                    "attributes": {
                        "productId": iap['id'],
                        "name": iap.get('displayName') or iap['id'].split('.')[-1].replace('_', ' ').title(),
                        "inAppPurchaseType": asc_type
                    },
                    "relationships": {
                        "app": {"data": {"type": "apps", "id": app_id}}
                    }
                }
            }
            asc_api("POST", "inAppPurchasesV2", token, data)
            results['created'].append(iap['id'])
        except Exception as e:
            results['errors'].append({"id": iap['id'], "error": str(e)})

    return results
```

---

## Phase 3: RevenueCat MCP Sync

Use RevenueCat MCP server with natural language commands:

### Check Project
```
"Show me my project details"
"List all apps in my RevenueCat project"
```

### Create Products
```
"Create a new product with identifier 'com.myapp.pro.monthly' for iOS"
"Create subscription product 'Premium Monthly' with ID 'com.myapp.premium.monthly'"
```

### Create Entitlements
```
"Create an entitlement called 'pro' with identifier 'pro'"
"Create 'premium_access' entitlement"
```

### Attach Products to Entitlements
```
"Attach product 'com.myapp.pro.monthly' to entitlement 'pro'"
"Link the premium monthly product to the premium features entitlement"
```

### Create Offerings
```
"Create an offering called 'default' with identifier 'default'"
"Add package 'monthly' to offering 'default' with product 'com.myapp.pro.monthly'"
```

### Multi-Platform Sync
```
"Create 'Premium Monthly' for both iOS and Android apps"
"Sync product configuration across all platforms"
```

---

## Full Sync Workflow

### Step 1: Scan Project
```
📂 Scanning project for IAP definitions...

Found 3 product(s):
  - com.myapp.credits.50 (consumable)
  - com.myapp.pro.monthly (auto-renewable)
  - com.myapp.pro.yearly (auto-renewable)
```

### Step 2: Sync to ASC
```
🍎 Syncing to App Store Connect...

  ✅ Created: com.myapp.credits.50
  ✅ Created: com.myapp.pro.monthly
  ✅ Created: com.myapp.pro.yearly
```

### Step 3: Sync to RevenueCat (via MCP)
```
🐱 Syncing to RevenueCat...

Agent commands:
1. "Create product 'com.myapp.credits.50' as consumable for iOS"
2. "Create product 'com.myapp.pro.monthly' as subscription for iOS"
3. "Create product 'com.myapp.pro.yearly' as subscription for iOS"
4. "Create entitlement 'pro' for premium access"
5. "Attach 'com.myapp.pro.monthly' to entitlement 'pro'"
6. "Attach 'com.myapp.pro.yearly' to entitlement 'pro'"
7. "Create offering 'default'"
8. "Add monthly package to 'default' with product 'com.myapp.pro.monthly'"
9. "Add annual package to 'default' with product 'com.myapp.pro.yearly'"
```

---

## Usage Examples

### Full sync
```
/aso-sync
```

### Sync specific app
```
/aso-sync MyApp --app-id 1234567890
```

### Preview without changes
```
/aso-sync --dry-run
```

### Sync only to ASC
```
/aso-sync --asc-only
```

### Sync only to RevenueCat
```
/aso-sync --rc-only
```

---

## RevenueCat MCP Setup

### Install MCP Server
```bash
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer YOUR_V2_API_KEY"
```

### Get API Key
1. Go to https://app.revenuecat.com
2. Select your project
3. Go to **API Keys**
4. Create new **V2 Secret Key** (write access)
5. Copy and use in command above

### Verify Setup
```
"Show me my RevenueCat project details"
```

---

## Output Example

```
🔄 Syncing GRW...
══════════════════════════════════════════════════

📂 Phase 1: Scanning project...
   Found 3 product(s)
   - com.furkancingoz.grw.credits.50 (consumable)
   - com.furkancingoz.grw.pro.monthly (auto-renewable)
   - com.furkancingoz.grw.pro.yearly (auto-renewable)

🍎 Phase 2: Syncing to App Store Connect...
   ✅ Created: 3
   ⏭️ Skipped: 0
   ❌ Errors: 0

🐱 Phase 3: Syncing to RevenueCat (via MCP)...
   ✅ Products created: 3
   ✅ Entitlements created: 1 (pro)
   ✅ Offering created: default
   ✅ Packages added: 2 (monthly, annual)

══════════════════════════════════════════════════
✅ Sync complete!
   Products: 3
   ASC: 3 created
   RevenueCat: 3 products, 1 entitlement, 1 offering
```

---

## Error Handling

### "RevenueCat MCP not found"
```bash
# Install MCP server
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer YOUR_V2_KEY"
```

### "No IAPs found in project"
- Add `.storekit` configuration file
- Or define products in Swift with recognizable IDs

### ASC 409 Conflict
- Product already exists, skipping

### RevenueCat "already exists"
- Product/entitlement already configured, skipping

---

## Agent Notes

- Scan project first to discover products
- Create ASC products before RevenueCat
- Use RevenueCat MCP for RC operations (natural language)
- Map subscription durations to RC packages automatically
- Be specific with product identifiers
- Make incremental changes, not bulk operations

---

## Sources

- [RevenueCat MCP Server](https://www.revenuecat.com/docs/tools/mcp)
- [RevenueCat MCP Setup](https://www.revenuecat.com/docs/tools/mcp/setup)
- [RevenueCat MCP Usage Examples](https://www.revenuecat.com/docs/tools/mcp/usage-examples)
