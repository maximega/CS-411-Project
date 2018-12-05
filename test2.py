import tweepy
import time

# This code outputs  followers fromm the inputted user.   

consumer_key = "" 
consumer_secret = "" 
access_token = ""
access_token_secret = "" 

accountvar = raw_input("Account:")

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

users = tweepy.Cursor(api.followers, screen_name=accountvar).items()

while True:
    try:
        user = next(users)
    except tweepy.TweepError:
        time.sleep(60*15)
        user = next(users)
    except StopIteration:
        break
    print "@" + user.screen_name