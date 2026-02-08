import boto3
import json
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BEDROCK_MODEL_ID
)

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def simplify_hindi(hindi_text: str, keywords: list) -> str:
    prompt = f"""
You are a Hindi language expert.

Hindi sentence:
{hindi_text}

Important keywords (context only):
{keywords}

Task:
- Replace uncommon or difficult Hindi words
- Use simple, commonly spoken Hindi
- Keep meaning unchanged
- Return ONLY the simplified Hindi sentence
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
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
    return result["content"][0]["text"].strip()
