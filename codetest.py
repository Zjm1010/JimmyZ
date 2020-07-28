from venv import logger
import threading
import csv
import tweepy
import numpy as np
import pandas as pd
import logging
import json


def time_fuc():
    CONSUMER_KEY = 
    CONSUMER_SECRET_KEY = 
    ACESS_TOKEN = 
    ACESS_TOKEN_SECRET = 

    # Keys connexion to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
    # Access tokens.
    auth.set_access_token(ACESS_TOKEN, ACESS_TOKEN_SECRET)
    api_tweeter = tweepy.API(auth)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    num_tweets = 1500
    top_num = 5  # Choosing Twitter with top 5 factor count
    retrieval_matrix1_factor = np.zeros((num_tweets, 1), dtype=int)
    retrieval_matrix2_id = []
    retrieval_matrix3_url = []
    keywords = "#Graphicdesign"

    count_a = 0
    for tweet in tweepy.Cursor(
            api_tweeter.search, q=keywords + "-filter:retweets" + "filter:media",
            count=num_tweets, lang="en", tweet_mode='extended'
    ).items(num_tweets):
        try:
            if not tweet.full_text.startswith("RT @"):
                if tweet.entities['media']:
                    if 'video' not in tweet.entities['media'][0]['media_url_https']:
                        retrieval_matrix1_factor[count_a] = tweet.retweet_count + tweet.favorite_count
                        retrieval_matrix2_id += tweet.id_str + ' '
                        retrieval_matrix2_id = ''.join(retrieval_matrix2_id)
                        a = 0
                        for image_url in tweet.entities['media']:
                            retrieval_matrix3_url += tweet.entities['media'][a]['media_url_https'] + ' '
                            a = a + 1
                        retrieval_matrix3_url = ''.join(retrieval_matrix3_url)
                        count_a = count_a + 1
        except:
            pass
    retrieval_matrix1_factor = retrieval_matrix1_factor.tolist()
    retrieval_matrix2_id = list(retrieval_matrix2_id.split(' '))
    retrieval_matrix3_url = list(retrieval_matrix3_url.split(' '))
    del (retrieval_matrix2_id[-1])
    del (retrieval_matrix3_url[-1])
    out = pd.DataFrame.from_dict({
        'factor': retrieval_matrix1_factor,
        'ID': retrieval_matrix2_id,
        'url': retrieval_matrix3_url}, orient='index')
    out = out.transpose()
    out = out.sort_values(by='factor', ascending=False).head(top_num)
    id_list = out['ID'].values.tolist()
    id_list = [str(integer) for integer in id_list]
    url_list = out['url'].values.tolist()
    url_list = [i for i in url_list if i]
    print(url_list)
    print(out['factor'])
    logger.info(f"Processing tweet id {url_list[0]}")

    a = 0
    try:
        for string in id_list:

            var_a = id_list[a]
            var_a = var_a.strip('[]')
            a = a + 1
            b = 0
            tweet = api_tweeter.get_status(var_a)
            print(tweet.text)
            try:
                for tags in tweet.entities['hashtags']:
                    keyword_tag = tweet.entities['hashtags'][b]['text']
                    b = b + 1
                    print(keyword_tag)
            except:
                print('No Hashtag')

    except:
        print('Less then ' + str(top_num) + ' tweets in the list')

    var_a = id_list[0]
    var_a = var_a.strip('[]')
    tweet = api_tweeter.get_status(var_a)
    if not tweet.favorited:
        # Mark it as Liked, since we have not done it yet
        try:
            tweet.favorite()
        except Exception as e:
            logger.error("Error on fav", exc_info=True)
    if not tweet.retweeted:
        # Retweet, since we have not retweeted it yet
        try:
            tweet.retweet()
        except Exception as e:
            logger.error("Error on fav and retweet", exc_info=True)
    timer = threading.Timer(17280, time_fuc)
    timer.start()


timer = threading.Timer(1, time_fuc)
timer.start()
