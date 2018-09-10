import tweepy
from virkamiesbot.settings import (TWITTER_A_TOKEN, TWITTER_A_TOKEN_SECRET,
                                   TWITTER_C_KEY,TWITTER_C_SECRET)

SEARCH_STRING = ''
# DEFAULT_TAGS = ['#Helsinki', '#Päätös']
DEFAULT_TAGS = ['#PÄIVÄNPÄÄTÖSTESTITESTI']

def handle_twitter(decision_data, twitter):
    tweet_content = generate_tweet_text(decision_data)
    tweet_successful = tweet(twitter, tweet_content)
    if tweet_successful:
        return True
    return False

def tweet(twitter_api, msg):
    try:
        response = twitter_api.update_status(msg)
    except tweepy.error.TweepError:
        return False
    if response != []:
        return True
    return False

# Generates tweet text
def generate_tweet_text(data):
    text = "{0}".format(shorten_message(data['content']))
    text += "\n{0}".format(data['permalink'])
    text += "\n%s" % tags_to_string(data['districts'])
    return text

# This function authenticates BOT and initializes twitter_api object
def initialize_twitter():
    twitter_auth = tweepy.OAuthHandler(TWITTER_C_KEY, TWITTER_C_SECRET)
    twitter_auth.set_access_token(TWITTER_A_TOKEN,TWITTER_A_TOKEN_SECRET)
    twitter_api = tweepy.API(twitter_auth)
    return twitter_api

# returns tags and default tags as a string
def tags_to_string(tags):
    tags_str = " ".join(DEFAULT_TAGS)
    tags_str += " {0}".format(tags)
    return tags_str

def shorten_message(msg):
    if len(msg) > 160:
        shortened = "%s..." % msg[0:157]
    else:
        shortened = msg
    return shortened