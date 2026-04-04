# /aso-legal Command

Generate legal documents (Privacy Policy, Terms of Use, EULA) for your app.

## Trigger
- `/aso-legal` or `/aso-legal privacy`
- "generate privacy policy", "create terms", "legal docs"

## Prerequisites
- App information (name, features, data collection)

---

## What It Does

```
📜 Legal Document Generator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Collect app information
2. Determine data practices
3. Generate customized documents
4. Output in multiple formats
```

---

## Usage

### Generate All Documents
```
/aso-legal --all
```

### Specific Document
```
/aso-legal privacy
/aso-legal terms
/aso-legal eula
```

### With Options
```
/aso-legal privacy --company "My Company" --email support@app.com
```

---

## Document Types

### 1. Privacy Policy
Required for all apps that collect any user data.

**Covers:**
- What data is collected
- How data is used
- Third-party sharing
- User rights (GDPR, CCPA)
- Data retention
- Contact information

### 2. Terms of Use / Terms of Service
Defines rules for using your app.

**Covers:**
- Acceptable use
- User responsibilities
- Intellectual property
- Disclaimers
- Limitation of liability
- Termination

### 3. EULA (End User License Agreement)
Software license agreement.

**Covers:**
- License grant
- Restrictions
- Ownership
- Updates
- Termination
- Warranty disclaimer

---

## Implementation

### Collect App Information

```python
def collect_app_info() -> dict:
    """
    Collect information needed for legal docs.

    Agent asks user:
    1. App name
    2. Company/Developer name
    3. Contact email
    4. Website URL
    5. What data does your app collect?
       - Personal info (name, email)
       - Location
       - Photos/Media
       - Health data
       - Financial data
       - Usage analytics
       - Device info
    6. Third-party services used?
       - Analytics (Firebase, Mixpanel)
       - Advertising (AdMob)
       - Authentication (Sign in with Apple)
       - Cloud services (AWS, Firebase)
    7. Does app have subscriptions/IAPs?
    8. Target audience (all ages, 13+, 17+)
    """
    pass

# Example info:
app_info = {
    "app_name": "CardTracker",
    "company_name": "My Company LLC",
    "contact_email": "support@cardtracker.app",
    "website": "https://cardtracker.app",
    "data_collected": [
        "email",
        "usage_analytics",
        "device_info"
    ],
    "third_party_services": [
        "firebase_analytics",
        "revenuecat"
    ],
    "has_subscriptions": True,
    "age_rating": "4+"
}
```

### Generate Privacy Policy

```python
def generate_privacy_policy(info: dict) -> str:
    """
    Generate customized Privacy Policy.

    Agent prompt:
    "Generate a Privacy Policy for this app:

     App: {app_name}
     Company: {company_name}
     Contact: {contact_email}

     Data Collected: {data_collected}
     Third-Party Services: {third_party_services}

     Requirements:
     - GDPR compliant (EU users)
     - CCPA compliant (California users)
     - Apple App Store compliant
     - Clear, readable language
     - Last updated date

     Output in Markdown format.
    "
    """
    pass
```

### Generate Terms of Use

```python
def generate_terms(info: dict) -> str:
    """
    Generate Terms of Use.

    Include:
    - Account terms (if applicable)
    - Acceptable use policy
    - Subscription/payment terms (if applicable)
    - Content guidelines
    - Intellectual property
    - Disclaimers
    - Limitation of liability
    - Dispute resolution
    - Changes to terms
    """
    pass
```

### Generate EULA

```python
def generate_eula(info: dict) -> str:
    """
    Generate End User License Agreement.

    Include:
    - License grant
    - Restrictions (no reverse engineering, etc.)
    - Ownership/IP rights
    - Updates and modifications
    - Term and termination
    - Warranty disclaimer
    - Limitation of liability
    - Governing law
    """
    pass
```

---

## Output Example

```
/aso-legal privacy --company "CardTracker LLC"

📜 Generating Privacy Policy...

Collecting information:
  App Name: CardTracker
  Company: CardTracker LLC
  Contact: support@cardtracker.app

Data Collection:
  ✓ Email address (account)
  ✓ Usage analytics
  ✓ Device information
  ✗ Location
  ✗ Health data
  ✗ Financial data

Third-Party Services:
  ✓ Firebase Analytics
  ✓ RevenueCat

Generating document...
─────────────────────────────────────────

# Privacy Policy

**Last Updated: April 4, 2026**

CardTracker LLC ("we", "our", or "us") operates the CardTracker
mobile application (the "App"). This Privacy Policy explains how
we collect, use, and protect your information.

## Information We Collect

### Information You Provide
- **Email Address**: When you create an account

### Information Collected Automatically
- **Usage Data**: How you interact with the App
- **Device Information**: Device type, OS version, app version

## How We Use Your Information
...

─────────────────────────────────────────
Characters: 4,521

Saved to: legal/privacy-policy.md

[1] Generate Terms of Use
[2] Generate EULA
[3] Generate all
[4] Edit this document
```

---

## Output Structure

```
legal/
├── privacy-policy.md
├── privacy-policy.html
├── terms-of-use.md
├── terms-of-use.html
├── eula.md
└── eula.html
```

---

## Compliance Checklist

### GDPR (EU)
- [ ] Legal basis for processing
- [ ] Right to access
- [ ] Right to deletion
- [ ] Data portability
- [ ] DPO contact (if applicable)

### CCPA (California)
- [ ] Categories of data collected
- [ ] Purpose of collection
- [ ] Right to know
- [ ] Right to delete
- [ ] Right to opt-out of sale

### Apple App Store
- [ ] Privacy Policy URL in app
- [ ] Privacy Policy URL in ASC
- [ ] Matches Privacy Nutrition Labels
- [ ] App Tracking Transparency (if applicable)

---

## Templates

### Simple Privacy Policy (No Data)
For apps that collect no personal data:

```markdown
# Privacy Policy

**Last Updated: [Date]**

[App Name] does not collect, store, or share any personal information.

## Analytics
We use anonymous analytics to understand app usage and improve our
service. This data cannot identify you personally.

## Contact
If you have questions, contact us at [email].
```

### Standard Privacy Policy
For apps with accounts and analytics:

```markdown
# Privacy Policy

**Last Updated: [Date]**

## Introduction
[Company] ("we") operates [App Name]. This policy explains our
data practices.

## Information We Collect
[List specific data types]

## How We Use Information
[List purposes]

## Information Sharing
[Third parties and why]

## Your Rights
[GDPR/CCPA rights]

## Data Security
[Security measures]

## Children's Privacy
[Age restrictions]

## Changes
[How updates are communicated]

## Contact
[Contact information]
```

---

## Legal Disclaimer

⚠️ **Important**: These generated documents are templates and starting
points. They are NOT legal advice. We recommend:

1. Review with a qualified attorney
2. Customize for your specific situation
3. Keep documents updated
4. Ensure compliance with all applicable laws

Different jurisdictions have different requirements. Consult legal
professionals for your specific needs.

---

## Agent Notes

- Ask about data collection first
- Customize based on app features
- Include all required sections
- Use clear, readable language
- Add last updated date
- Provide both .md and .html formats
- Remind user to review with attorney
