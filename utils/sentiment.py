import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
}

def analyze_sentiment(text):

    try:

        if not isinstance(text, str):

            return "neutral", 0

        if text.strip() == "":

            return "neutral", 0

        payload = {
            "inputs": text[:512]
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        result = response.json()

        if isinstance(result, list):

            prediction = max(
                result[0],
                key=lambda x: x["score"]
            )

            label = prediction["label"].lower()

            score = round(
                prediction["score"],
                2
            )

            return label, score

        return "neutral", 0

    except Exception:

        return "neutral", 0