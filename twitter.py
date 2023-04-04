import base64
import json
import pandas as pd
import streamlit as st
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
from datetime import datetime
import csv

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter"]
collection = db['twitter']

document = {
    'hashtag': 'tweet',
    'data': 'twitter'
}

collection.insert_one(document)

# Define functions
def scrape_tweets(keyword, start_date, end_date,num_tweets):
    # convert start and end dates to datetime objects
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.max.time())
    search_words = keyword + ' since:' + start_date.strftime('%Y-%m-%d') + ' until:' + end_date.strftime('%Y-%m-%d')
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_words} since:{start_date.date()} until:{end_date.date()}').get_items()):
        if i >= num_tweets:
            break
        tweets.append({
            "date": tweet.date,
            "id": tweet.id,
            "url": tweet.url,
            "content": tweet.rawContent,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        })
    db["tweets"].insert_one({
        "Scraped Word": search_words,
        "Scraped Date": start_date.strftime("%d-%m-%Y"),
        "Scraped Data": tweets
    })
    return tweets

# Streamlit app
import streamlit as st

#Creating heading and aligning it to center and giving a grey background color
st.markdown("""
<style>
h1 {
    text-align: center;
    background-color: grey;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.write("<h1>Twitter Data Scraper</h1>", unsafe_allow_html=True)


# Get user input using form
with st.form("Input Form"):  
  
    #st.markdown
    keyword = st.text_input("Enter keyword or hashtag")
    start_date = st.date_input("Start Date")
    #start_date = datetime.strptime(start_date, '%Y-%m-%d')
    start_date_str = datetime.strftime(start_date, '%d-%m-%Y')
    #st.write("Start Date (DD-MM-YYYY):", start_date_str)

    end_date = st.date_input("End Date")
# Convert the end_date object to a string in the format "DD-MM-YYYY"
    end_date_str = datetime.strftime(end_date, '%d-%m-%Y')
    limit = st.number_input("Enter number of tweets to scrape", value=100)
    submit_button = st.form_submit_button(label='Submit')

# Scrape tweets and display in table
if submit_button:
    tweets_list = []
    tweets = scrape_tweets(keyword, start_date, end_date, limit)
    for tweet in tweets:
        tweets_list.append([tweet['date'], tweet['id'], tweet['url'], tweet['content'], tweet['user'], tweet['reply_count'], tweet['retweet_count'], tweet['language'], tweet['source'], tweet['like_count']])
    df = pd.DataFrame(tweets_list, columns=['Date', 'ID', 'URL', 'Content', 'User', 'Reply Count', 'Retweet Count', 'Language', 'Source', 'Like Count'])
    st.write(df)
    
    # Upload data to MongoDB
    if len(df) > 0:
        db = client['twitter']
        collection = db['twitter']
        collection.insert_many(df.to_dict('records'))
        st.write("Data uploaded to MongoDB!")
    else:
        st.write("No data to upload!")

# Add a button to upload the data to the database
tweets=[]
if st.button("Upload to Database"):
    # Insert the tweets into the database
    for tweet in tweets:
        db.tweets.insert_one(tweet)
    st.success("Data uploaded to database!")

## Add a button to download the data in CSV format
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter"]
collection = db["tweets"]

# Define function to convert dataframe to CSV and create download link
def create_download_link(df, tweets):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{tweets}">Download CSV</a>'
    return href

# Get the data from MongoDB
data = list(collection.find())

# Convert the data to a Pandas dataframe
df = pd.DataFrame(data)

# Add a button to download the data in CSV format
if st.button("Download CSV"):
    st.markdown(create_download_link(df, "tweets.csv"), unsafe_allow_html=True)


# Add a button to download the data in JSON format
if st.button("Download JSON"):
# Download the tweets as JSON
  json_data = json.dumps(tweets, indent=4)
  b64 = base64.b64encode(json_data.encode()).decode()
  href = f'<a href="data:file/json;base64,{b64}" download="tweets.json">Download JSON</a>'
  st.markdown(href, unsafe_allow_html=True)




