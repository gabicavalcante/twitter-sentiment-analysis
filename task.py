import tweepy
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

search_words = "covid+covid19+pandemic -filter:retweets"
tweets_count = 1

def get_tweets(date_until: str, geocode: str):
    tweets = tweepy.Cursor(api.search,
        q=search_words,
        lang="en",
        geocode=geocode,
        until=date_until).items(tweets_count)
    
    data = [tweet._json for tweet in tweets]
    print(data)
    # TODO: inset in mongo