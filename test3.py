import tweepy

consumer_key = "" 
consumer_secret = "" 
access_token = ""
access_token_secret = "" 

def authenticate():
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


api = authenticate()
# api = tweepy.API(auth)

followers = []
user = api.get_user("gwuah_")
for user in user.followers():
    followers.append(user.screen_name)

ptint(followers)
print('hi')