import pandas as pd
import streamlit as st
from utils.sentiment import analyze_sentiment
import plotly.express as px
from utils.insights import generate_insights

st.set_page_config(page_title='AI Feedback Dashboard',layout='wide')

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border-radius: 12px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

st.title('AI Feedback Analysis Dashboard')
st.write('Upload a CSV dataset to start analysis.')

uploaded_file=st.file_uploader("Upload CSV File",type=['csv'])

#Csv loading function
def load_csv(file):
    encodings=['utf-8','latin1','ISO-8859-1']

    for encoding in encodings:
        try:
            df=pd.read_csv(file,encoding=encoding,on_bad_lines='skip')
            return df
        except Exception: 
            continue

    return None

#file upload
if uploaded_file is not None:
    try:
        df=load_csv(uploaded_file)

        if df is None:
            st.error('Unable to read CSV file. Please upload a valid dataset')
            st.stop()

        if df.empty:
            st.error('Uploaded CSV file is empty.')
            st.stop()

        st.success('File uploaded successfully')

        #Dataset metrics
        col1,col2,col3=st.columns(3)
        col1.metric('Rows', df.shape[0])
        col2.metric('Columns', df.shape[1])
        col3.metric('Missing Values', df.isnull().sum().sum())
        st.divider()

        #Preview dataset
        st.subheader('Dataset Preview')
        st.dataframe(df.head(),use_container_width=True)

        #Cols section
        st.subheader('Select Review Columns')
        review_column=st.selectbox('Choose a column containing feedback/reviews',df.columns)
        st.success(f'Selected Column: {review_column}')

        analyze_button=st.button('Run sentiment analysis')

        #Sentiment Logic
        if analyze_button:
            with st.spinner('Analyzing Sentiments'):
                sentiments=[]
                confidence_scores=[]
                reviews=df[review_column].fillna('')

                for review in reviews:
                    label,score=analyze_sentiment(review)

                    sentiments.append(label)
                    confidence_scores.append(score)

                df['Sentiment']=sentiments
                df['Confidence Score']=confidence_scores

                st.success('Sentiment Analysis Completed!')

                tab1,tab2,tab3=st.tabs(["Dataset","Dashboard","AI Insights"])

                with tab1:
                    st.subheader('Analyzed Dataset')
                    st.dataframe(df.head(100),use_container_width=True)
                
                #Dashboard Logic - Sentiment Count
                with tab2:
                    sentiment_counts=df['Sentiment'].value_counts()
                    positive_count=sentiment_counts.get('positive',0)
                    negative_count=sentiment_counts.get('negative',0)
                    neutral_count=sentiment_counts.get('neutral',0)

                    st.subheader('Sentiment Overview')

                    kpi1,kpi2,kpi3=st.columns(3)
                    kpi1.metric("Positive Reviews", positive_count)
                    kpi2.metric("Neutral Reviews", neutral_count)
                    kpi3.metric("Negative Reviews", negative_count)

                    ##Pie chart
                    pie_chart = px.pie(names=sentiment_counts.index,values=sentiment_counts.values,title="Sentiment Distribution")
                    pie_chart.update_layout(height=400)

                    #Bar chart
                    bar_chart = px.bar(x=sentiment_counts.index,y=sentiment_counts.values,title="Sentiment Count", 
                                        labels={
                                        "x": "Sentiment",
                                        "y": "Count"
                                        })
                    bar_chart.update_layout(height=400)
                    
                    chart1,chart2=st.columns(2)
                    with chart1:
                        st.plotly_chart(pie_chart,use_container_width=True)

                    with chart2:
                        st.plotly_chart(bar_chart,use_container_width=True)

                    #Positive reviews
                    st.divider()
                    review_col1, review_col2 = st.columns(2)

                    with review_col1:
                        st.subheader("🟢 Top Positive Reviews")

                        positive_reviews = df[
                            df['Sentiment'] == 'positive'
                        ][review_column].head(3)

                        for review in positive_reviews:
                            st.success(review)

                    #Negative Review
                    with review_col2:
                        st.subheader("🔴 Top Negative Reviews")
                        negative_reviews = df[
                            df['Sentiment'] == 'negative'
                        ][review_column].head(3)

                        for review in negative_reviews:
                            st.error(review)

                #Gemini AI Integration Insight
                with tab3:
                    st.subheader('AI Generated Insights')

                    with st.spinner('Generating AI Insights...'):
                        sample_reviews=" ".join(
                            df[review_column].fillna("").astype(str).head(50).tolist()
                    )
                        insights=generate_insights(sample_reviews)
                        st.markdown(insights)
        
    
    except pd.errors.ParserError:
        st.error('CSV Parsing failed. Please upload a clean CSV file.')


    except UnicodeDecodeError:
        st.error('Encoding issue is detected. Please save CSV as UTF-8')

    except Exception as e:
        st.error('Something went wrong while processing the file')

        st.exception(e)

