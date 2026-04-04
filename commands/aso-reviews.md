# /aso-reviews Command

Manage App Store reviews with AI-powered response suggestions.

## Trigger
- `/aso-reviews` or `/aso-reviews AppName`
- "check reviews", "respond to reviews", "review management"

## Prerequisites
- API Key configured (`~/.aso/credentials.json`)
- App published on App Store

---

## What It Does

```
💬 Review Management Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Fetch recent reviews
2. Analyze sentiment
3. Generate AI response suggestions
4. Post responses to ASC
```

---

## Usage

### View Recent Reviews
```
/aso-reviews list
/aso-reviews list --rating 1-3
```

### Respond to Review
```
/aso-reviews respond REVIEW_ID
/aso-reviews respond --all-negative
```

### Analytics
```
/aso-reviews stats
```

---

## Implementation

### Fetch Reviews

```python
from lib.asc_api import ASCClient, generate_token

def get_customer_reviews(app_id: str, limit: int = 50) -> list:
    """Fetch customer reviews from ASC."""
    token = generate_token()
    client = ASCClient(token)

    # Note: customerReviews endpoint
    response = client._request(
        "GET",
        f"apps/{app_id}/customerReviews?limit={limit}&sort=-createdDate"
    )
    return response.get("data", [])

def filter_reviews(reviews: list, min_rating: int = None, max_rating: int = None) -> list:
    """Filter reviews by rating."""
    filtered = []
    for review in reviews:
        rating = review["attributes"]["rating"]
        if min_rating and rating < min_rating:
            continue
        if max_rating and rating > max_rating:
            continue
        filtered.append(review)
    return filtered

# Get negative reviews (1-3 stars)
reviews = get_customer_reviews(app_id)
negative = filter_reviews(reviews, max_rating=3)
```

### Analyze Sentiment

```python
def analyze_review(review: dict) -> dict:
    """Analyze review sentiment and topics."""
    attrs = review["attributes"]

    analysis = {
        "id": review["id"],
        "rating": attrs["rating"],
        "title": attrs.get("title", ""),
        "body": attrs.get("body", ""),
        "territory": attrs.get("territory", ""),
        "created": attrs.get("createdDate", ""),
        "sentiment": None,
        "topics": [],
        "priority": None
    }

    # Sentiment based on rating
    if attrs["rating"] <= 2:
        analysis["sentiment"] = "negative"
        analysis["priority"] = "high"
    elif attrs["rating"] == 3:
        analysis["sentiment"] = "neutral"
        analysis["priority"] = "medium"
    else:
        analysis["sentiment"] = "positive"
        analysis["priority"] = "low"

    # Extract topics (AI can enhance this)
    body = attrs.get("body", "").lower()
    if "crash" in body or "bug" in body:
        analysis["topics"].append("technical_issue")
    if "slow" in body or "performance" in body:
        analysis["topics"].append("performance")
    if "feature" in body or "wish" in body:
        analysis["topics"].append("feature_request")
    if "price" in body or "expensive" in body:
        analysis["topics"].append("pricing")

    return analysis
```

### Generate Response

```python
def generate_response(review: dict, app_context: str = None) -> str:
    """
    AI generates professional response.

    Agent prompt:
    "Generate a professional, empathetic response to this App Store review.

     Review:
     Rating: {rating}/5
     Title: {title}
     Body: {body}

     App context: {app_context}

     Guidelines:
     - Be empathetic and professional
     - Thank them for feedback
     - Address specific concerns
     - Offer solution or next steps
     - Keep under 5970 characters
     - Don't be defensive
     - Don't promise specific features/timelines
    "
    """
    # Claude generates naturally
    pass

# Example responses by sentiment:

# Negative (1-2 stars):
"""
Hi [Name],

Thank you for taking the time to share your feedback. We're sorry to hear
about the issues you've experienced.

We take these concerns seriously and our team is actively working on
improvements. If you could reach out to support@app.com with more details,
we'd love to help resolve this for you.

We appreciate your patience and hope to earn a better rating in the future.

Best regards,
The [App] Team
"""

# Neutral (3 stars):
"""
Thank you for your review! We're glad you're finding value in [App], and
we appreciate your suggestions for improvement.

We're always working to make the app better, and feedback like yours helps
us prioritize what matters most to our users.

If you have more ideas, feel free to reach out at support@app.com.

Thanks for being part of our community!
"""

# Positive (4-5 stars):
"""
Thank you so much for your kind review! 🙏

We're thrilled that you're enjoying [App]. Your support means the world
to us and motivates our team to keep improving.

If you ever have suggestions or need help, we're always here at
support@app.com.

Happy [using the app]!
"""
```

### Post Response

```python
def post_review_response(review_id: str, response_text: str):
    """Post response to App Store review."""
    token = generate_token()
    client = ASCClient(token)

    data = {
        "data": {
            "type": "customerReviewResponses",
            "attributes": {
                "responseBody": response_text
            },
            "relationships": {
                "review": {
                    "data": {"type": "customerReviews", "id": review_id}
                }
            }
        }
    }

    return client._request("POST", "customerReviewResponses", data)
```

---

## Output Example

```
/aso-reviews list --rating 1-3

💬 Recent Reviews - MyApp
─────────────────────────────────────────

⭐ 1/5 - "App keeps crashing"
   ID: abc123 | US | 2 days ago
   "Every time I try to save, the app crashes..."
   Topics: technical_issue
   Priority: HIGH

⭐ 2/5 - "Too expensive"
   ID: def456 | UK | 3 days ago
   "I like the app but the subscription is too much..."
   Topics: pricing
   Priority: HIGH

⭐ 3/5 - "Good but needs work"
   ID: ghi789 | DE | 5 days ago
   "Nice concept but missing some features..."
   Topics: feature_request
   Priority: MEDIUM

─────────────────────────────────────────
Total: 12 reviews | Negative: 3 | Avg: 3.8⭐

[1] Respond to abc123
[2] Respond to all negative
[3] View all reviews
```

```
/aso-reviews respond abc123

💬 Generating Response...

Review:
⭐ 1/5 - "App keeps crashing"
"Every time I try to save, the app crashes. I've lost data twice now."

Suggested Response:
─────────────────────────────────────────
Hi there,

Thank you for bringing this to our attention, and we sincerely apologize
for the frustration caused by these crashes.

This is not the experience we want you to have. Our team is
investigating this issue as a top priority. In the meantime, could you
please email us at support@app.com? We'd like to:

1. Help recover any lost data if possible
2. Get more details about when the crashes occur
3. Provide you with a workaround while we fix this

We truly appreciate your patience and will work hard to resolve this quickly.

Best regards,
The MyApp Team
─────────────────────────────────────────
Characters: 612/5970 ✅

[1] Post this response
[2] Edit response
[3] Generate alternative
[4] Skip
```

---

## Review Stats

```
/aso-reviews stats

📊 Review Analytics - MyApp (Last 30 days)
─────────────────────────────────────────

Rating Distribution:
⭐⭐⭐⭐⭐ ████████████████░░░░ 68%
⭐⭐⭐⭐   ████████░░░░░░░░░░░░ 18%
⭐⭐⭐     ████░░░░░░░░░░░░░░░░  8%
⭐⭐       ██░░░░░░░░░░░░░░░░░░  4%
⭐         █░░░░░░░░░░░░░░░░░░░  2%

Average: 4.5⭐ | Total: 156 reviews

Top Topics:
  🐛 Technical Issues: 12
  💡 Feature Requests: 8
  💰 Pricing: 5
  🚀 Performance: 3

Response Rate: 78% (negative reviews)
Avg Response Time: 18 hours
```

---

## Response Guidelines

### DO
- Thank the reviewer
- Acknowledge their concern
- Offer concrete help (email, steps)
- Be empathetic and professional
- Keep it concise

### DON'T
- Be defensive
- Promise specific features/dates
- Argue or blame the user
- Use corporate jargon
- Copy-paste generic responses

---

## Character Limit

**Review Response: 5970 characters**

Recommended: 300-600 characters for readability.

---

## Agent Notes

- Prioritize negative reviews (1-3 stars)
- Respond within 24-48 hours
- Personalize each response
- Track response effectiveness
- Learn from common complaints
- Escalate technical issues to dev team
