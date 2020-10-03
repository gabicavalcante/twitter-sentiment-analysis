import tweepy
from config import *
from datetime import date, timedelta

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# search words and the date_since date as variables
search_words = "covid+covid19+pandemic -filter:retweets"
date_until = date.today() - timedelta(days=1)
date_fst3 = [date.today() - timedelta(days=d) for d in range(1, 4)]
date_lst3 = [date.today() - timedelta(days=d) for d in range(4, 7)]

tweets_count = 150

geocodes = dict(
    geocode_ny = "40.714353,-74.00597299999998,20km",
    geocode_washington = "47.725428,-120.644006,200km",
    geocode_california = "35.958501,-119.723561,2000km",
    geocode_texas = "32.101866,-98.727558,200km",
    geocode_uk = "54.088088,-1.971351,500km"
)
# # q=f"{search_words} -filter:retweets until:{date_until}"

# data = []
for geocode in geocodes:
    for date_until in first:
        tweets = tweepy.Cursor(api.search,
                    q=search_words,
                    lang="en",
                    geocode=geocodes["geocode_minnesota"],
                    until=date_until).items(tweets_count)
        data.append(tweet._json)