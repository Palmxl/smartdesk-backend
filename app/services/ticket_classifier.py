def classify_ticket(text: str):

    text = text.lower()

    priority = "Low"
    sentiment = "Neutral"
    category = "General"

    # PRIORITY

    if (
        "urgent" in text
        or "error" in text
        or "failed" in text
    ):
        priority = "High"

    # SENTIMENT

    negative_words = [
        "angry",
        "terrible",
        "bad",
        "horrible",
        "molesto",
    ]

    if any(word in text for word in negative_words):
        sentiment = "Negative"

    # CATEGORY

    if "login" in text:
        category = "Authentication"

    elif "payment" in text:
        category = "Billing"

    elif "server" in text:
        category = "Infrastructure"

    return {
        "priority": priority,
        "sentiment": sentiment,
        "category": category,
    }