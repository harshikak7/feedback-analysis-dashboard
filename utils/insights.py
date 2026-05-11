from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_insights(reviews_text):
    try:
        prompt = f"""
        Analyze the following customer reviews.

        Give:
        1. Overall Summary
        2. Positive Trends
        3. Negative Trends
        4. Suggestions for improvement

        Reviews:
        {reviews_text}
        """

        response = client.chat.completions.create(

            model="llama3-8b-8192",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception:

        return """
AI Insights Temporarily Unavailable.
"""