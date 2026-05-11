import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

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
            timeout=15
        )

        result = response.json()

        if isinstance(result, list):

            best_prediction = max(
                result[0],
                key=lambda x: x["score"]
            )

            label = best_prediction["label"].lower()

            score = round(
                best_prediction["score"],
                2
            )

            return label, score

        return "neutral", 0

    except Exception as e:

        print(e)

        return "neutral", 0