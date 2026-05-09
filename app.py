import pandas as pd
import streamlit as st
from utils.sentiment import analyze_sentiment
import plotly.express as px

st.set_page_config(page_title='AI Feedback Dashboard',layout='wide')
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
        st.success(f'Selected Column:{review_column}')

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
                st.subheader('Analyzed Dataset')

                st.dataframe(df.head(100),use_container_width=True)
                
                #Dashboard Logic - Sentiment Count
                sentiment_counts=df['Sentiment'].value_counts()

                positive_count=sentiment_counts.get('positive',0)
                negative_count=sentiment_counts.get('negative',0)
                neutral_count=sentiment_counts.get('neutral',0)

                st.divider()
                st.subheader('Sentiment Overview')

                kpi1,kpi2,kpi3=st.columns(3)
                kpi1.metric("Positive Reviews", positive_count)
                kpi2.metric("Neutral Reviews", neutral_count)
                kpi3.metric("Negative Reviews", negative_count)

                ##Pie chart
                pie_chart = px.pie(names=sentiment_counts.index,values=sentiment_counts.values,title="Sentiment Distribution")
                st.plotly_chart(pie_chart,use_container_width=True)

                #Bar chart
                bar_chart = px.bar(x=sentiment_counts.index,y=sentiment_counts.values,title="Sentiment Count", 
                                    labels={
                                       "x": "Sentiment",
                                       "y": "Count"
                                    })
                
                st.plotly_chart(bar_chart,use_container_width=True)
    
    except pd.errors.ParserError:
        st.error('CSV Parsing failed. Please upload a clean CSV file.')


    except UnicodeDecodeError:
        st.error('Encoding issue is detected. Please save CSV as UTF-8')

    except Exception as e:
        st.error('Something went wrong while processing the file')

        st.exception(e)

