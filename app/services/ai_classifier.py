from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    device=-1
)

summary_pipeline = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1
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

def summarize_ticket(
    text: str
):

    if len(text.split()) < 20:

        return text

    result = summary_pipeline(
        text,
        max_length=30,
        min_length=5,
        do_sample=False
    )

    return result[0]["summary_text"]