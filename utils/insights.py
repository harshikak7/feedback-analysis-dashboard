def generate_insights(df):

    insights = {}

    insights["top_city"] = df["city"].mode()[0]

    sentiment_counts = df["sentiment"].value_counts(normalize=True)

    insights["positive_percent"] = sentiment_counts.get("Positive", 0) * 100

    insights["negative_percent"] = sentiment_counts.get("Negative", 0) * 100

    return insights