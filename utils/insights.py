import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv('GEMINI_API_KEY')
)

model=genai.GenerativeModel("models/gemini-2.0-flash-lite")

def generate_insights(reviews_text):
    try:
        prompt=f""" Analyze the following customer reviews.

        Give:
        1. Overall Summary
        2. Positive Trends
        3. Negative Trends
        4. Suggestions for improvements

        Reviews: {reviews_text}"""

        response=model.generate_content(prompt)
        return response.text

    except Exception as e:
        return """AI insights are temporarily unavailable due to API quota limits. Please try again in a few minutes."""