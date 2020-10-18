from task import get_tweets
from datetime import date, timedelta

from rq import Queue, Worker
from redis import Redis

redis_conn = Redis(host="0.0.0.0", port=6379, db=0)
queue = Queue("default", connection=redis_conn) 

date_until = date.today() - timedelta(days=1)
date_fst3 = [date.today() - timedelta(days=d) for d in range(1, 4)]
date_lst3 = [date.today() - timedelta(days=d) for d in range(4, 7)]

geocodes = dict(
    geocode_ny = "40.714353,-74.00597299999998,20km",
    geocode_washington = "47.725428,-120.644006,200km",
    geocode_california = "35.958501,-119.723561,2000km",
    geocode_texas = "32.101866,-98.727558,200km",
    geocode_uk = "54.088088,-1.971351,500km"
)
# # q=f"{search_words} -filter:retweets until:{date_until}"

if __name__ == "__main__":
    for geocode in geocodes.values():
        for date_until_1, date_until_2  in zip(date_fst3, date_lst3):
            queue.enqueue(get_tweets, date_until_1, geocode)
            print("%s, %s, %s" %(job, geocode, date_until))

            queue.enqueue_in(timedelta(minutes=20), get_tweets, date_until_2, geocode)
            print("%s, %s, %s" %(job, geocode, date_until))