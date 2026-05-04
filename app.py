import streamlit as st
import pandas as pd
import plotly.express as px

from sentiment import get_sentiment
from insights import generate_insights
from utils.keyword_extractor import extract_keywords

# 🔍 Auto-detect text column
def find_text_column(df):
    possible_cols = ["review", "text", "comment", "feedback", "content"]

    for col in df.columns:
        if col.lower().strip() in possible_cols:
            return col

    return None

st.set_page_config(page_title="Feedback Analyzer", layout="wide")
st.title("Feedback Analytics Dashboard")

# 📂 Upload file
uploaded_file = st.file_uploader(
    "Upload your feedback dataset (CSV format)",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a CSV file to begin analysis")
    st.stop()


# 📊 Load dataset
df = pd.read_csv(uploaded_file)

st.subheader("Dataset Preview")
st.dataframe(df.head())

# 🧠 Column selection (smart)
text_col = find_text_column(df)

if text_col:
    st.success(f"Auto-detected column: {text_col}")
else:
    text_col = st.selectbox(
        "Select the column containing reviews",
        df.columns
    )

# ✅ Apply sentiment
df["sentiment"] = df[text_col].astype(str).apply(get_sentiment)

st.subheader("Sentiment Analysis Result")
st.dataframe(df.head())


# 📊 Sentiment Chart
sentiment_chart = px.pie(
    df,
    names="sentiment",
    title="Sentiment Distribution"
)

# 📊 Optional charts (only if columns exist)

charts = []

if "rating" in df.columns:
    rating_chart = px.histogram(df, x="rating", title="Rating Distribution")
    charts.append(rating_chart)

if "city" in df.columns:
    city_chart = px.histogram(
        df,
        x="city",
        color="sentiment",
        title="City-wise Feedback"
    )
    charts.append(city_chart)

# 📊 Layout
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(sentiment_chart, use_container_width=True)

if charts:
    with col2:
        st.plotly_chart(charts[0], use_container_width=True)

# 🔑 Keywords
st.subheader("Top Keywords")

keywords = extract_keywords(df[text_col].dropna().astype(str))

for word, count in keywords:
    st.write(f"{word} : {count}")

# 🧠 Insights
st.subheader("Auto Insights")

try:
    insights = generate_insights(df)

    st.success(f"Most feedback from: {insights.get('top_city', 'N/A')}")
    st.success(f"Positive feedback: {insights.get('positive_percent', 0):.2f}%")
    st.success(f"Negative feedback: {insights.get('negative_percent', 0):.2f}%")

except:
    st.warning("Insights could not be generated for this dataset")