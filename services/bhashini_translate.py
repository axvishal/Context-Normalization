import requests
from config.settings import (
    BHASHINI_API_KEY,
    BHASHINI_USER_ID,
    BHASHINI_API_URL
)

def translate_en_to_hi(text: str) -> str:
    payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "en",
                        "targetLanguage": "hi"
                    },
                    "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                }
            }
        ],
        "inputData": {
            "input": [{"source": text}]
        }
    }

    headers = {
        "Authorization": BHASHINI_API_KEY,
        "userID": BHASHINI_USER_ID,
        "Content-Type": "application/json"
    }

    response = requests.post(BHASHINI_API_URL, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["pipelineResponse"][0]["output"][0]["target"]
