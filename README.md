# Feedback Analysis Dashboard

A flexible dashboard for analyzing user feedback from CSV files.  
It supports different dataset formats and generates basic insights without breaking.

## Features

- Upload any CSV dataset  
- Automatic / manual selection of review column  
- Sentiment analysis (Positive / Negative)  
- Charts:
  - Sentiment distribution  
  - Rating distribution (if available)  
  - City-wise analysis (if available)  
- Keyword extraction  
- Basic insights (top city, sentiment %)  
- Handles missing columns safely  

## Tech Stack

Python, Streamlit, Pandas, Plotly

## Run Locally

```bash
git clone https://github.com/harshikak7/feedback-analysis-dashboard.git
cd feedback-analysis-dashboard

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```
## Author

Harshika Kolekar
https://github.com/harshikak7