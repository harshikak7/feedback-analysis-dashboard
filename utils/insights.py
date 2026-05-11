import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv('GEMINI_API_KEY')
)

model=genai.GenerativeModel("gemini-2.0-flash")

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

        if response.text:
            return response.text
        return f"AI Insights Temporarily Unavailable The Gemini API is currently rate-limited or unavailable. Please try again later."

    except Exception:
        return f"AI Insights Temporarily Unavailable The Gemini API is currently rate-limited or unavailable. Please try again later."