import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
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
            "retweet_count": dict_data["retweet_count"],
            "quote_count": dict_data["retweet_count"],
            "reply_count": dict_data["reply_count"],
            "favorite_count": dict_data["favorite_count"],
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

    # a = {'created_at': 'Mon Sep 21 13:52:03 +0000 2020', 'id': 1308041303188439040, 'id_str': '1308041303188439040', 'text': 'RT @_alannne: janeiro, fevereiro, covid-19, dezembro', 'truncated': False, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [{'screen_name': '_alannne', 'name': 'a', 'id': 2792519413, 'id_str': '2792519413', 'indices': [3, 12]}], 'urls': []}, 'metadata': {'iso_language_code': 'pt', 'result_type': 'recent'}, 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 1129634014103576576, 'id_str': '1129634014103576576', 'name': 'cadelinha do noah beck', 'screen_name': 'BiancaMeloo1', 'location': 'Acre, Brasil', 'description': 'ɐpᴉʌ ɐɥuᴉɯ ɐp ɹoɯɐ o ɐɹᴉʌ ǝ ɐๅǝʇ ɐ noɹᴉʌ ǝnb ɐʇᴉǝʌoɹdⱯ ✊🏼✊🏽✊🏾✊🏿 @Corinthians', 'url': 'https://t.co/bXNM8d2egg', 'entities': {'url': {'urls': [{'url': 'https://t.co/bXNM8d2egg', 'expanded_url': 'http://Instagram.com/byalimamelo', 'display_url': 'Instagram.com/byalimamelo', 'indices': [0, 23]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 1177, 'friends_count': 1101, 'listed_count': 0, 'created_at': 'Sat May 18 06:25:11 +0000 2019', 'favourites_count': 10837, 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'verified': False, 'statuses_count': 9811, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'F5F8FA', 'profile_background_image_url': None, 'profile_background_image_url_https': None, 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1303885750400962562/1yZHfO7S_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1303885750400962562/1yZHfO7S_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/1129634014103576576/1600060761', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'retweeted_status': {'created_at': 'Sun Sep 20 22:19:34 +0000 2020', 'id': 1307806633947430918, 'id_str': '1307806633947430918', 'text': 'janeiro, fevereiro, covid-19, dezembro', 'truncated': False, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': []}, 'metadata': {'iso_language_code': 'pt', 'result_type': 'recent'}, 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 2792519413, 'id_str': '2792519413', 'name': 'a', 'screen_name': '_alannne', 'location': 'spxrj', 'description': 'in beyoncé we trust', 'url': 'https://t.co/WuFkZ0OAOT', 'entities': {'url': {'urls': [{'url': 'https://t.co/WuFkZ0OAOT', 'expanded_url': 'http://instagram.com/iyabalaces', 'display_url': 'instagram.com/iyabalaces', 'indices': [0, 23]}]}, 'description': {'urls': []}}
