from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    device=-1
)

generator_pipeline = pipeline(
    "text-generation",
    model="distilgpt2",
    device=-1
)

def classify_ticket_ai(
    text: str
):

    result = sentiment_pipeline(
        text
    )[0]

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

    shortened = text[:120]

    return shortened + "..."

def generate_ticket_response(
    text: str
):

    prompt = f"""
Customer issue:
{text}

Write a short professional
customer support response.
Keep it under 3 sentences.
Do not repeat phrases.
"""

    result = generator_pipeline(

        prompt,

        max_new_tokens=60,

        do_sample=True,

        temperature=0.7,

        top_k=50,

        top_p=0.95,

        repetition_penalty=1.4,

        num_return_sequences=1,

        truncation=True,

        pad_token_id=50256
    )

    generated = (
        result[0]
        ["generated_text"]
    )

    response = generated.replace(
        prompt,
        ""
    ).strip()

    response = (
        response[:300]
    )

    return response