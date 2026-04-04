# /aso-iap Command

Set up In-App Purchases and Subscriptions for App Store Connect.

## Trigger
- `/aso-iap` or `/aso-iap AppName`
- "set up IAPs", "configure subscriptions", "add in-app purchases"

## Workflow

### 1. Check Authentication
```bash
test -f ~/.blitz/asc-agent/web-session.json && echo "SESSION_EXISTS" || echo "NO_SESSION"
```

If NO_SESSION: Call `asc_web_auth` MCP tool first.

### 2. Get App ID
```bash
asc apps list | grep -i "APP_NAME"
```

### 3. List Current IAPs & Subscriptions

Use iris API to list all IAPs and subscriptions:

```python
# List subscription groups with subscriptions
GET https://appstoreconnect.apple.com/iris/v1/apps/{APP_ID}/subscriptionGroups?include=subscriptions&limit=300

# List in-app purchases
GET https://appstoreconnect.apple.com/iris/v1/apps/{APP_ID}/inAppPurchasesV2?limit=300
```

Show user:
- Product ID
- Name
- State (READY_TO_SUBMIT, APPROVED, etc.)
- Whether attached to current version

### 4. Ask User What To Do

Options:
1. **Create new IAP** → Guide through creation
2. **Create new Subscription** → Guide through subscription group + product
3. **Attach existing to version** → Use attach workflow
4. **List all** → Show current state

### 5. Attach to Version

For items in `READY_TO_SUBMIT` state:

**Subscriptions:**
```python
POST https://appstoreconnect.apple.com/iris/v1/subscriptionSubmissions
{
  "data": {
    "type": "subscriptionSubmissions",
    "attributes": {"submitWithNextAppStoreVersion": true},
    "relationships": {
      "subscription": {"data": {"type": "subscriptions", "id": "SUB_ID"}}
    }
  }
}
```

**In-App Purchases:**
```python
POST https://appstoreconnect.apple.com/iris/v1/inAppPurchaseSubmissions
{
  "data": {
    "type": "inAppPurchaseSubmissions",
    "attributes": {"submitWithNextAppStoreVersion": true},
    "relationships": {
      "inAppPurchaseV2": {"data": {"type": "inAppPurchases", "id": "IAP_ID"}}
    }
  }
}
```

### 6. Verify

After attachment, show updated state:
- Which items are attached
- Which items are pending
- Submission readiness status

## Common IAP Patterns

### Credit Packs (Consumable)
```
- 5 Credits: $0.99 (com.app.credits.5)
- 15 Credits: $1.99 (com.app.credits.15)
- 50 Credits: $4.99 (com.app.credits.50)
```

### Subscription Tiers
```
- Monthly Pro: $4.99/month
- Yearly Pro: $39.99/year (save 33%)
- Lifetime: $99.99 one-time
```

## Error Handling

### 409 "Already set to submit"
Item is already attached. This is OK - treat as success.

### 401 Not Authorized
Session expired. Call `asc_web_auth` MCP tool to re-authenticate.

### "FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION"
Use iris API (not public API) - it supports `submitWithNextAppStoreVersion`.

## Agent Notes

- Always list IAPs/subs first to show current state
- Confirm with user before attaching
- Use iris API for attach (not public ASC API)
- Never print session cookies
- Rate limit: 350ms between requests
