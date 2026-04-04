# /aso-manage - Reviews & Legal Documents

Manage App Store reviews and generate legal documents.

## Usage

```bash
/aso-manage reviews               # View & respond to reviews
/aso-manage reviews --negative    # Focus on negative reviews
/aso-manage legal                 # Generate legal docs
/aso-manage legal privacy         # Privacy Policy only
```

## Subcommands

### reviews - Review Management

```bash
/aso-manage reviews               # List recent reviews
/aso-manage reviews --negative    # 1-3 star reviews
/aso-manage reviews --respond ID  # Respond to specific
/aso-manage reviews --stats       # Analytics
```

### legal - Legal Documents

```bash
/aso-manage legal                 # Generate all
/aso-manage legal privacy         # Privacy Policy
/aso-manage legal terms           # Terms of Use
/aso-manage legal eula            # EULA
```

---

## Review Management

### List Reviews
```
/aso-manage reviews

💬 Recent Reviews - MyApp
─────────────────────────────────────────

⭐ 1/5 - "App keeps crashing"
   ID: abc123 | US | 2 days ago
   Priority: HIGH

⭐ 2/5 - "Too expensive"
   ID: def456 | UK | 3 days ago
   Priority: HIGH

⭐ 5/5 - "Love this app!"
   ID: ghi789 | DE | 5 days ago
   Priority: LOW

─────────────────────────────────────────
Total: 12 | Negative: 3 | Avg: 3.8⭐
```

### AI Response Suggestions

```
/aso-manage reviews --respond abc123

Review: ⭐ 1/5 - "App keeps crashing"

Suggested Response:
─────────────────────────────────────────
Hi there,

Thank you for your feedback. We're sorry about
the crashes you've experienced.

Our team is investigating this issue. Could you
email support@app.com with more details? We'd
love to help resolve this.

Best regards,
The MyApp Team
─────────────────────────────────────────

[1] Post response
[2] Edit
[3] Generate alternative
```

### Response Guidelines

**DO:**
- Thank the reviewer
- Acknowledge concerns
- Offer help (email, steps)
- Be empathetic

**DON'T:**
- Be defensive
- Promise features/dates
- Argue
- Use generic copy-paste

---

## Legal Documents

### Generate All
```bash
/aso-manage legal --company "My Company" --email support@app.com
```

### Privacy Policy
Required for apps collecting any data.

**Sections:**
- Information collected
- How it's used
- Third-party sharing
- User rights (GDPR, CCPA)
- Data retention
- Contact info

### Terms of Use
Defines rules for using your app.

**Sections:**
- Acceptable use
- User responsibilities
- Intellectual property
- Disclaimers
- Limitation of liability

### EULA
Software license agreement.

**Sections:**
- License grant
- Restrictions
- Ownership
- Updates
- Termination
- Warranty disclaimer

---

## Legal Templates

### No Data Collected
```markdown
# Privacy Policy

[App Name] does not collect any personal information.

## Analytics
We use anonymous analytics to improve the app.
This data cannot identify you.

## Contact
Questions? Email [email]
```

### Standard App
```markdown
# Privacy Policy

Last Updated: [Date]

## Information We Collect
- Email address (account)
- Usage analytics
- Device information

## How We Use Information
- Provide app functionality
- Improve user experience
- Send important updates

## Your Rights
- Access your data
- Delete your account
- Opt-out of marketing

## Contact
[Company] - [Email]
```

---

## Output

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
- [ ] Right to access/delete
- [ ] Data portability

### CCPA (California)
- [ ] Categories of data
- [ ] Right to know/delete
- [ ] Opt-out of sale

### Apple
- [ ] Privacy Policy URL in app
- [ ] Matches Privacy Labels

---

## Examples

```bash
# Respond to negative reviews
/aso-manage reviews --negative --respond-all

# Generate privacy policy
/aso-manage legal privacy --company "MyApp LLC"

# Full legal suite
/aso-manage legal --company "MyApp LLC" --email hi@myapp.com
```

---

## Disclaimer

⚠️ Generated documents are templates. Review with an attorney
for your specific situation and jurisdiction.
