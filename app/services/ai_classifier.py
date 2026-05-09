from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis"
)

def classify_ticket_ai(
    text: str
):

    result = sentiment_pipeline(text)[0]

    label = result["label"]

    priority = "Low"

    if (
        "error" in text.lower()
        or "urgent" in text.lower()
        or label == "NEGATIVE"
    ):
        priority = "High"

    category = "General"

    if (
        "payment" in text.lower()
    ):
        category = "Billing"

    elif (
        "login" in text.lower()
    ):
        category = "Authentication"

    sentiment = (
        "Negative"
        if label == "NEGATIVE"
        else "Positive"
    )

    return {
        "priority": priority,
        "sentiment": sentiment,
        "category": category,
    }