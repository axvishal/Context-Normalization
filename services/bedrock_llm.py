import boto3
import json
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BEDROCK_MODEL_ID
)

# Create Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def simplify_hindi(hindi_text: str, keywords: list) -> list:
    """
    Returns:
    [
        {
            "english_word": "...",
            "hindi_word": "...",
            "simplified_hindi": "..."
        }
    ]
    """

    prompt = f"""
You are a Hindi-English linguistic expert.

Hindi sentence:
{hindi_text}

Relevant English keywords (only meaningful words):
{keywords}

Task:
1. From the Hindi sentence, identify only complex/formal/colloquial words.
2. Match them to the corresponding English keyword.
3. Provide a simpler Hindi substitute.

IMPORTANT:
- Ignore pronouns, auxiliary verbs, articles, and common functional words.
- Only consider meaningful nouns, adjectives, or adverbs.
- Do NOT rewrite the sentence.
- Return ONLY valid JSON.

Output format:

[
  {{
    "english_word": "extremely",
    "hindi_word": "अत्यधिक",
    "simplified_hindi": "बहुत"
  }}
]
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    text_output = result["content"][0]["text"].strip()

    try:
        parsed = json.loads(text_output)
        if isinstance(parsed, list):
            return parsed
        return []
    except Exception:
        return []
