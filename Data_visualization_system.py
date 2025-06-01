import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS



st.title("Data Visualization Project Using Streamlit And Python")
st.sidebar.title("Data Visualization Project Using Streamlit And Python")

st.markdown("This application is a streamlit dashboard used to analyze sentiments of tweets 𝕏")
st.sidebar.markdown("This application is a streamlit dashboard used to analyze sentiments of tweets 𝕏")

DATA_URL = ("D:\\Python Learning\\create-interactive-dashboards-with-streamlit-and-python\\Doc\\Tweets.csv")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()
#st.write(data)


st.sidebar.subheader("Show Random Tweets")
random_tweets = st.sidebar.radio("sentiment",("positive","neutral","negative"))
st.sidebar.markdown(data.query("airline_sentiment== @random_tweets")[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiments")
select = st.sidebar.selectbox("Visualization type",["Histogram","Pie Chart"],key="1")

sentiment_count = data["airline_sentiment"].value_counts()
#st.write(sentiment_count)
sentiment_count = pd.DataFrame({"sentiment":sentiment_count.index,"Tweets":sentiment_count.values})

if not st.sidebar.checkbox("Hide",True):
    st.markdown("Number Of Tweets By Sentiments")
    if select == "Histogram":
        fig_0 = px.bar(sentiment_count,x="sentiment",y="Tweets",color="sentiment",height=500)
        st.plotly_chart(fig_0)
    else:
        fig_1 = px.pie(sentiment_count,names="sentiment",values="Tweets")
        st.plotly_chart(fig_1)


st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of the day",0,23)
modified_data = data[data["tweet_created"].dt.hour==hour]

if  st.sidebar.checkbox("Show Map",False,key="2"):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown(f"{len(modified_data)} tweets btn {hour}:00 and {(hour + 1) % 24}:00")
    st.map(modified_data)

if st.sidebar.checkbox("Show Raw Data",False,key="3"):
    st.write(modified_data)

st.sidebar.subheader("Breakdown airlines by sentiments")
choice = st.sidebar.multiselect("Pick Airline",("Us Airways","United","American","Southwest","Delta","Virgin America"),key="0")

if len(choice)>0:
   

    choice_data = data[data.airline.isin (choice)]
    fig_choice = px.histogram(choice_data,x="airline",y="airline_sentiment",color="airline_sentiment",histfunc="count",
                 facet_col="airline_sentiment",height=500,width=500,labels={"airline_sentiment:tweets"})
    st.subheader("Breakdown Airlines Analysis By Sentiments")
    st.plotly_chart(fig_choice)

    st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud for which sentiment?",("positive","neutral","negative"))

if not st.sidebar.checkbox("Close", True, key="4"):
    st.subheader("Word cloud for %s sentiment" % word_sentiment)
    
    df = data[data["airline_sentiment"] == word_sentiment]
    words = " ".join(df["text"])
    processed_words = " ".join([
        word for word in words.split()
        if "http" not in word and not word.startswith("@") and word != "RT"
    ])

    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        background_color="white",
        height=640,
        width=800
    ).generate(processed_words)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)