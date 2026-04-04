# /aso-sync Command

Sync IAP/Subscription configuration between Project, App Store Connect, and RevenueCat.

## Trigger
- `/aso-sync` or `/aso-sync AppName`
- "sync IAPs", "sync subscriptions", "sync products"

## What It Does

```
📂 Project Code          🍎 App Store Connect       🐱 RevenueCat
─────────────────        ────────────────────       ─────────────
StoreKit Config    ←→    IAP Products         ←→    Products
Products.swift     ←→    Subscriptions        ←→    Entitlements
Pricing            ←→    Price Schedule       ←→    Offerings
```

## Prerequisites

### 1. App Store Connect API Key
```bash
# Already configured via /aso-setup
cat ~/.aso/credentials.json
```

### 2. RevenueCat API Keys
```bash
cat > ~/.aso/revenuecat.json << 'EOF'
{
  "v1ApiKey": "sk_xxxxxxxxxxxxxxxxxxxx",
  "projectId": "proj_xxxxxxxxxxxx",
  "appId": {
    "ios": "app_xxxxxxxxxxxx",
    "android": "app_xxxxxxxxxxxx"
  }
}
EOF
chmod 600 ~/.aso/revenuecat.json
```

Get keys from: https://app.revenuecat.com/settings/api-keys

## Workflow

### Phase 1: Project Scan

Scan project for IAP definitions:

```python
import os, json, re, plistlib

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
                            'type': product['type'],  # consumable, non-consumable, subscription
                            'price': product.get('price', 0),
                            'source': 'storekit'
                        })

    # 2. Check Swift files for product IDs
    product_pattern = r'["\']([a-z0-9_.]+\.(subscription|credits|pro|premium|lifetime)[a-z0-9_.]*)["\']'
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
                                'type': 'unknown',
                                'source': 'swift'
                            })

    return iaps

# Usage
iaps = scan_project_iaps('/path/to/project')
for iap in iaps:
    print(f"{iap['id']}: {iap['type']}")
```

### Phase 2: App Store Connect Sync

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

    # Get existing IAPs
    existing = asc_api("GET", f"apps/{app_id}/inAppPurchasesV2", token)
    existing_ids = {p["attributes"]["productId"] for p in existing["data"]}

    results = {"created": [], "skipped": [], "errors": []}

    for iap in iaps:
        if iap['id'] in existing_ids:
            results['skipped'].append(iap['id'])
            continue

        # Map type
        iap_type_map = {
            'consumable': 'CONSUMABLE',
            'non-consumable': 'NON_CONSUMABLE',
            'non_consumable': 'NON_CONSUMABLE',
            'subscription': 'NON_RENEWING_SUBSCRIPTION',
            'auto-renewable': 'AUTO_RENEWABLE_SUBSCRIPTION'
        }
        asc_type = iap_type_map.get(iap.get('type', '').lower(), 'CONSUMABLE')

        try:
            data = {
                "data": {
                    "type": "inAppPurchases",
                    "attributes": {
                        "productId": iap['id'],
                        "name": iap.get('name', iap['id'].split('.')[-1].replace('_', ' ').title()),
                        "inAppPurchaseType": asc_type,
                        "reviewNote": f"Synced from project"
                    },
                    "relationships": {
                        "app": {"data": {"type": "apps", "id": app_id}}
                    }
                }
            }
            result = asc_api("POST", "inAppPurchasesV2", token, data)
            results['created'].append(iap['id'])
        except Exception as e:
            results['errors'].append({"id": iap['id'], "error": str(e)})

    return results
```

### Phase 3: RevenueCat Sync

Sync to RevenueCat:

```python
import json, os, urllib.request

def rc_api(method, endpoint, data=None):
    """Make RevenueCat API request."""
    with open(os.path.expanduser("~/.aso/revenuecat.json")) as f:
        config = json.load(f)

    url = f"https://api.revenuecat.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {config['v1ApiKey']}",
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def sync_to_revenuecat(iaps, app_id_ios):
    """Sync products to RevenueCat."""

    with open(os.path.expanduser("~/.aso/revenuecat.json")) as f:
        config = json.load(f)

    project_id = config['projectId']

    results = {"created": [], "skipped": [], "errors": []}

    for iap in iaps:
        try:
            # Create product in RevenueCat
            data = {
                "store_identifier": iap['id'],
                "app_id": app_id_ios,
                "type": map_rc_type(iap.get('type', 'consumable'))
            }

            result = rc_api("POST", f"projects/{project_id}/products", data)
            results['created'].append(iap['id'])

        except urllib.error.HTTPError as e:
            if e.code == 409:  # Already exists
                results['skipped'].append(iap['id'])
            else:
                results['errors'].append({"id": iap['id'], "error": str(e)})

    return results

def map_rc_type(iap_type):
    """Map IAP type to RevenueCat type."""
    type_map = {
        'consumable': 'consumable',
        'non-consumable': 'non_consumable',
        'non_consumable': 'non_consumable',
        'subscription': 'subscription',
        'auto-renewable': 'subscription'
    }
    return type_map.get(iap_type.lower(), 'consumable')
```

### Phase 4: Create Entitlements & Offerings

```python
def create_entitlements(project_id, iaps):
    """Create entitlements for products."""

    # Group by feature
    entitlements = {}
    for iap in iaps:
        # Extract entitlement from product ID
        # e.g., com.app.pro.monthly → pro
        parts = iap['id'].split('.')
        entitlement_name = None

        for part in ['pro', 'premium', 'unlimited', 'credits']:
            if part in parts:
                entitlement_name = part
                break

        if entitlement_name:
            if entitlement_name not in entitlements:
                entitlements[entitlement_name] = []
            entitlements[entitlement_name].append(iap['id'])

    # Create each entitlement
    for name, products in entitlements.items():
        data = {
            "lookup_key": name,
            "display_name": name.title()
        }
        result = rc_api("POST", f"projects/{project_id}/entitlements", data)

        # Attach products to entitlement
        for product_id in products:
            rc_api("POST", f"projects/{project_id}/entitlements/{name}/products", {
                "product_id": product_id
            })

    return entitlements

def create_default_offering(project_id, iaps):
    """Create default offering with all products."""

    # Create offering
    offering_data = {
        "lookup_key": "default",
        "display_name": "Default Offering"
    }
    offering = rc_api("POST", f"projects/{project_id}/offerings", offering_data)

    # Create packages
    subscriptions = [p for p in iaps if 'subscription' in p.get('type', '').lower()]

    package_map = {
        'monthly': '$rc_monthly',
        'yearly': '$rc_annual',
        'weekly': '$rc_weekly',
        'lifetime': '$rc_lifetime'
    }

    for sub in subscriptions:
        for key, rc_key in package_map.items():
            if key in sub['id'].lower():
                rc_api("POST", f"projects/{project_id}/offerings/default/packages", {
                    "lookup_key": rc_key,
                    "product_id": sub['id']
                })
                break

    return offering
```

## Full Sync Command

```python
def full_sync(project_path, app_id, app_name):
    """Run full sync: Project → ASC → RevenueCat"""

    print(f"🔄 Syncing {app_name}...")
    print("=" * 50)

    # Phase 1: Scan project
    print("\n📂 Phase 1: Scanning project...")
    iaps = scan_project_iaps(project_path)
    print(f"   Found {len(iaps)} product(s)")
    for iap in iaps:
        print(f"   - {iap['id']} ({iap.get('type', 'unknown')})")

    if not iaps:
        print("   ⚠️ No IAPs found in project")
        return

    # Phase 2: Sync to ASC
    print("\n🍎 Phase 2: Syncing to App Store Connect...")
    token = generate_token()
    asc_results = sync_to_asc(app_id, iaps, token)
    print(f"   ✅ Created: {len(asc_results['created'])}")
    print(f"   ⏭️ Skipped: {len(asc_results['skipped'])}")
    print(f"   ❌ Errors: {len(asc_results['errors'])}")

    # Phase 3: Sync to RevenueCat
    print("\n🐱 Phase 3: Syncing to RevenueCat...")

    if not os.path.exists(os.path.expanduser("~/.aso/revenuecat.json")):
        print("   ⚠️ RevenueCat not configured. Run /aso-setup --revenuecat")
        return

    with open(os.path.expanduser("~/.aso/revenuecat.json")) as f:
        rc_config = json.load(f)

    rc_results = sync_to_revenuecat(iaps, rc_config['appId']['ios'])
    print(f"   ✅ Created: {len(rc_results['created'])}")
    print(f"   ⏭️ Skipped: {len(rc_results['skipped'])}")
    print(f"   ❌ Errors: {len(rc_results['errors'])}")

    # Phase 4: Create entitlements & offerings
    print("\n🎁 Phase 4: Creating entitlements & offerings...")
    entitlements = create_entitlements(rc_config['projectId'], iaps)
    print(f"   Created {len(entitlements)} entitlement(s)")

    offering = create_default_offering(rc_config['projectId'], iaps)
    print("   Created default offering")

    # Summary
    print("\n" + "=" * 50)
    print("✅ Sync complete!")
    print(f"   Products: {len(iaps)}")
    print(f"   ASC: {len(asc_results['created'])} created")
    print(f"   RevenueCat: {len(rc_results['created'])} created")
    print(f"   Entitlements: {len(entitlements)}")
```

## Usage Examples

### Sync from current project
```
/aso-sync
```

### Sync specific app
```
/aso-sync MyApp --app-id 1234567890
```

### Sync only to ASC
```
/aso-sync --asc-only
```

### Sync only to RevenueCat
```
/aso-sync --rc-only
```

### Preview without changes
```
/aso-sync --dry-run
```

## Credentials Setup

### RevenueCat Setup
```
/aso-setup --revenuecat

1. Go to: https://app.revenuecat.com/settings/api-keys
2. Copy your V1 API Key (starts with sk_)
3. Note your Project ID (starts with proj_)
4. Note your App ID (starts with app_)
```

## Output Example

```
🔄 Syncing GRW...
==================================================

📂 Phase 1: Scanning project...
   Found 3 product(s)
   - com.furkancingoz.grw.credits.50 (consumable)
   - com.furkancingoz.grw.pro.monthly (subscription)
   - com.furkancingoz.grw.pro.yearly (subscription)

🍎 Phase 2: Syncing to App Store Connect...
   ✅ Created: 3
   ⏭️ Skipped: 0
   ❌ Errors: 0

🐱 Phase 3: Syncing to RevenueCat...
   ✅ Created: 3
   ⏭️ Skipped: 0
   ❌ Errors: 0

🎁 Phase 4: Creating entitlements & offerings...
   Created 1 entitlement(s)
   Created default offering

==================================================
✅ Sync complete!
   Products: 3
   ASC: 3 created
   RevenueCat: 3 created
   Entitlements: 1 (pro)
```

## Error Handling

### "No IAPs found in project"
- Add `.storekit` configuration file
- Or define products in Swift with recognizable IDs

### RevenueCat 401
- Check API key at `~/.aso/revenuecat.json`
- Ensure V1 API key (not V2)

### ASC 409 Conflict
- Product already exists, skipping

## Agent Notes

- Always scan project first
- Preview changes with --dry-run
- Create ASC products before RevenueCat
- Map subscription durations to RC packages
- Never expose API keys
