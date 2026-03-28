import streamlit as st
import pandas as pd
import plotly.express as px

from sentiment import get_sentiment
from insights import generate_insights
from utils.keyword_extractor import extract_keywords


st.set_page_config(
    page_title="Smart Feedback Analytics Dashboard",
    layout="wide"
)

st.title("Smart Feedback Analytics Dashboard")


uploaded_file = st.file_uploader(
    "Upload your feedback dataset (CSV format)",
    type=["csv"]
)


# Stop app if no file uploaded

if uploaded_file is None:

    st.info("Please upload a CSV file to begin analysis")

    st.stop()


# Load dataset

df = pd.read_csv(uploaded_file)


st.subheader("Dataset Preview")

st.dataframe(df)


# Sentiment detection

df["sentiment"] = df["review"].apply(get_sentiment)


st.subheader("Sentiment Analysis Result")

st.dataframe(df)


# Create charts

sentiment_chart = px.pie(
    df,
    names="sentiment",
    title="Sentiment Distribution"
)


rating_chart = px.histogram(
    df,
    x="rating",
    title="Rating Distribution"
)


city_chart = px.histogram(
    df,
    x="city",
    color="sentiment",
    title="City-wise Feedback"
)


keyword_chart_data = extract_keywords(df["review"])


# Layout: 2 charts per row

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(sentiment_chart, use_container_width=True)

with col2:
    st.plotly_chart(rating_chart, use_container_width=True)


col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(city_chart, use_container_width=True)

with col4:

    st.subheader("Top Keywords")

    for word, count in keyword_chart_data:
        st.write(f"{word} : {count}")


# Auto insights section

st.subheader("Auto Insights")

insights = generate_insights(df)

st.success(f"Most feedback from: {insights['top_city']}")

st.success(
    f"Positive feedback: {insights['positive_percent']:.2f}%"
)

st.success(
    f"Negative feedback: {insights['negative_percent']:.2f}%"
)