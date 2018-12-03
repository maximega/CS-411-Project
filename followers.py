import tweepy
import time

# This code outputs  followers fromm the inputted user.   

consumer_key = "aL3FbY1z6yMH0nrIEk4z8H2I3" 
consumer_secret = "BcCBeyzHHteohqrQqCNWW06nQS8M2A5BH6ChPZS3yoex0BzWb2" 
access_token = "956264951156498432-6JE2kpBQ3tNVXeYYeHl255Og8O7MNne"
access_token_secret = "Vf6hul4q0lqlZ1WztKeRcGSSRWCxL2iXjBrBjv1INL3pE" 

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