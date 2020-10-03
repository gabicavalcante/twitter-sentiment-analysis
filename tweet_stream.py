import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API

from textblob import TextBlob
from elasticsearch import Elasticsearch

# import twitter keys and tokens
from config import *

from pymongo import MongoClient

client = MongoClient()

db = client.ml
collection = db.sentiment

# create instance of elasticsearch
es = Elasticsearch()


class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):
        # decode json
        dict_data = json.loads(data)

        if not "text" in dict_data:
            return True
        
        # pass tweet into TextBlob
        tweet = TextBlob(dict_data["text"])

        # output sentiment polarity
        print(tweet.sentiment.polarity)

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # output sentiment
        print(sentiment)

        # add text and sentiment info to elasticsearch
        tweet_dict = {
            "screen_name": dict_data["user"]["screen_name"],
            "username": dict_data["user"]["name"],
            "date": dict_data["created_at"],
            "message": dict_data["text"],
            "polarity": tweet.sentiment.polarity,
            "subjectivity": tweet.sentiment.subjectivity,
            "sentiment": sentiment,
            "lang": dict_data["lang"],
            # "retweet_count": dict_data["retweet_count"],
            # "quote_count": dict_data["retweet_count"],
            # "reply_count": dict_data["reply_count"],
            # "favorite_count": dict_data["favorite_count"],
            "followers_count": dict_data["user"]["followers_count"],
            "friends_count": dict_data["user"]["friends_count"],
            "filter_level": dict_data["filter_level"],
            "source": dict_data["source"],
            "geo": dict_data["geo"],
            "coordinates": dict_data["coordinates"],
            "place": dict_data["place"],
        }

        es.index(index="sentiment", doc_type="test-type", body=tweet_dict)

        inserted_id = collection.insert_one(tweet_dict).inserted_id
        print(f"inserted id: {inserted_id}")
        return True

    # on failure
    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream 
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    stream.filter(track=["covid19", "covid", "covid-19", "pandemic"])