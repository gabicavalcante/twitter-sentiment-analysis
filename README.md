# twitter-sentiment-analysis

Using as reference the blog post [twitter sentiment python docker elasticsearch kibana](https://realpython.com/twitter-sentiment-python-docker-elasticsearch-kibana/).

### run

1. twitter api

To run the project you need to register an application at [twitter apps](http://apps.twitter.com/). Get the `consumer key` and `consumer secret` and create an `access token` under the *Keys and Access Tokens* tab. There is a file `config.template.py`, copy it and rename to `config.py`. Add your credentials in this file.

```
consumer_key = "add_your_consumer_key"
consumer_secret = "add_your_consumer_secret"
access_token = "add_your_access_token"
access_token_secret = "add_your_access_token_secret"
```

2. streaming and processing tweets
   
We are using the [Tweepy](https://www.tweepy.org) to grab the tweets. You can see the code in `sentimental.py` file, there we connect to twitter api and filter the data by the keywords `[covid, covid19, covid-19, pandemia]`. 

The next step is calculate sentimental analysis using [Textblog](http://textblob.readthedocs.org/en/dev/), determine if the overall sentiment is positive, negative or neutral. At the end, the tweet data is added to the Elasticsearch DB and Mongo DB.

3. store the data

To run mongo, kibana and the elasticsearch:

```
$ docker-compose up
```

To run the python script:

```
$ pip install -r requirements.txt
$ python sentimental.py
```
