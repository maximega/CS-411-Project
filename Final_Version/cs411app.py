import random
import flask
import requests
import json
import sys
import base64
from flask import Flask, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL

try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse

mysql = MySQL()
app = Flask(__name__)

# ----------------- API ACCESS KEYS & INFO ----------------
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['spotify_id']
CLIENT_SECRET = CLIENT['spotify_secret']
EBAY_ACCESS_TOKEN = CLIENT['ebay_token']

# ----------------- DB CONFIGURATION ----------------
app.config['MYSQL_DATABASE_USER'] = CLIENT['sql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = CLIENT['sql_pwd']
app.config['MYSQL_DATABASE_DB'] = CLIENT['sql_db']
app.config['MYSQL_DATABASE_HOST'] = CLIENT['sql_host']
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

# ----------------- SPOTIFY OAUTH & TOKEN INFO SET UP ----------------
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
app.secret_key = 'bff89419b87b4e088f5f0b458b1536ce'

REDIRECT_URI = "http://127.0.0.1:8081/callback/"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID
}

# ----------------- SPOTIFY OAUTH URL FORMATTING ----------------
URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                for key, val in list(auth_query_parameters.items())])
#(above libraries only work for python 3+)

# ----------------- SPOTIFY OAUTH URL ----------------
AUTH_URL = "https://accounts.spotify.com/authorize/?{}".format(URL_ARGS)

# ----------------- APP HOME PAGE ----------------
@app.route('/')
def profile():
    # ----------------- IF USER LOGGED IN ADD USER ID TO DB IF NOT ALREADY PRESENT ----------------
    if 'auth_header' in session:
        auth_header = session['auth_header']
        uid = session['user_id']

        profile_data = get_users_profile(auth_header)

        query = "SELECT users.user_id FROM users WHERE users.user_id = '%s'" % (uid)
        cursor.execute(query)
        check = [item for item in cursor]

        if (not check):
            query = "INSERT INTO users VALUES (%s)" % (uid)
            cursor.execute(query)
            conn.commit()
        
        if valid_token(profile_data):
            return render_template('home.html')
    # ----------------- IF USER NOT LOGGED IN SEND TO PROFILE PAGE FOR OAUTH ----------------
    else:
        return render_template('profile.html')

# ----------------- VALIDATE TOKEN ----------------
def valid_token(resp):
    return resp is not None and not 'error' in resp

# ----------------------- AUTH API PROCEDURE -------------------------
@app.route("/auth")
def auth():
    return redirect(AUTH_URL)

# ----------------------- AUTH CALLBACK PROCEDURE -------------------------
@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = authorize(auth_token)
    session['auth_header'] = auth_header
    profile_data = get_users_profile(auth_header)
    session['user_id'] = profile_data['id']
    return profile()

# ----------------------- CREATE AUTH TOKEN FOR SPOTIFY API CALLS -------------------------
def authorize(auth_token):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    #python 3 or above required
    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)
    
    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]


    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header

# ----------------------- GET CURRENT USER'S PROFILE -------------------------
def get_users_profile(auth_header):
    url = "https://api.spotify.com/v1/me"
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# ------------ ALL OF THE BELOW FUNCTIONS REDIRECT TO THE PROFILE ROUTE IF USER IS NOT LOGGED IN --------------
@app.route('/home', methods=['GET'])
def home():
    if 'auth_header' not in session:
        return render_template('profile.html')

    return render_template('home.html')

# ----------------------- DELETE A GIFT ENTRY FROM YOUR WISHLIST -------------------------
@app.route('/deleteitem', methods=['POST', 'GET'])
def deleteitem():
    if 'auth_header' not in session:
        return render_template('profile.html')

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        item_id = int(request.form.get('item_id'))
        delete_query = "DELETE FROM item WHERE item.uid = '%s' AND item.item_id = %d" % (user_id, item_id)
        cursor.execute(delete_query)
        conn.commit()
        return flask.redirect('/wishlist')\

# ----------------------- EBAY ITEM LISTING PAGE -------------------------
@app.route('/result', methods=['GET', 'POST'])
def result():
    # ----------------------- GET WHEN ALISTING EBAY ITEMS -------------------------
    if 'auth_header' not in session:
        return render_template('profile.html')
    if request.method == 'GET':
        error = None
        sort = None
        rand = None
        responseList = request.args
        # ----------------------- SORT HANDLES SORTING ITEMS BY ASCENDING/DESCENDING PRICES -------------------------
        if len(responseList) > 1:
            item = list(responseList.values())[0]
            sort = list(responseList.values())[1]
        elif len(responseList) == 1:
            item = list(responseList.values())[0]
        return make_ebay_search(item, sort, rand,'result.html')
    # ----------------------- POST WHEN ADDING A SPECIFIC ITEM TO YOUR WISHLIST -------------------------
    else:
        title = request.form.get('title')
        price = float(request.form.get('price'))
        currency = request.form.get('currency') 
        link = request.form.get('link')
        recipient = request.form.get('recipient')
        user_id = session['user_id']
        query = "INSERT INTO item (title, price, currency, link, recipient, uid) VALUES ('%s', %f, '%s', '%s', '%s', '%s')" % (title, price, currency, link, recipient, user_id)
        cursor.execute(query)
        conn.commit()
        return flask.redirect('/wishlist')

# ----------------------- ROUTE FOR GENERATING YOUR WISHLIST -------------------------
@app.route('/wishlist', methods=['GET'])
def generateWishList():
    if 'auth_header' not in session:
        return render_template('profile.html')

    user_id = session['user_id']
    query = "SELECT title, price, currency, link, recipient, item_id, uid FROM item WHERE item.uid = '%s'" % (user_id)
    cursor.execute(query)
    gifts = [item for item in cursor]
    return render_template('wishlist.html', gifts=gifts)

# ----------------------- ROUTE WHEN ENTERED VALUE INTO SPOTIFY SEARCH BAR -------------------------
@app.route('/spotify', methods=['GET', 'POST'])
def spotify():
    if 'auth_header' not in session:
        return render_template('profile.html')

    error = None
    sort = None
    rand = None
    responseList = request.args
    if len(responseList) > 2:
        track = list(responseList.values())[0]
        sort = list(responseList.values())[1]
        rand = int(list(responseList.values())[2])
    elif len(responseList) == 2:
        track = list(responseList.values())[0]
        rand = int(list(responseList.values())[1])
    elif len(responseList) == 1:
        track = list(responseList.values())[0]
    # ----------------------- IF SEARCHED FOR TRACK DOES NOT EXIST -------------------------
    if not track:
        error = True
        return render_template('home.html', error=error, search_term=track)
    # ----------------------- IF ITEM NOT PRESENT IN CACHE MAKE API CALL -------------------------
    if track not in session:
        artists = make_spotify_search(track)
        session[track] = artists
    # ----------------------- IF ITEM PRESENT IN CACHE RETREIEVE FROM CACHE -------------------------
    else:
        artists = session[track]
    if(not artists):
        error = True
        return render_template('home.html', error=error, search_term=track)

    # -------- SELECT RANDOM ARTIST FROM LIST OF ARTISTS ASSOCIATED WITH ENTERED TRACK --------
    # -------- IF YOU ARE JUST SORTING, THEN RESORT ON THE SAME ARTIST YOU JUST ENTERED, SO RANDOMIZATION IS SKIPPED --------
    if(rand):
        artists = session[track]
        item = artists[rand]
    else:
        ceiling = len(artists) -1
        rand = random.randint(0, ceiling)
        item = artists[rand]

    return make_ebay_search(item, sort, rand, 'spotify.html')

# -------- HELPER FUNCTION FOR MAKING EBAY API CALL FOR SPECIFIED ITEM, AND SPECIFIED SORTING CRITERIA --------
def make_ebay_search(item, sort, rand, render_str):
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search?q=" + item
    if sort:
        if sort == "Ascending":
            url+= "&sort=price"
        if sort == "Descending":
            url += "&sort=-price"

    url += "&limit=100"
    headers = {'Authorization': EBAY_ACCESS_TOKEN}
    r = requests.get(url, headers=headers)
    dictionary = r.json()
    # ------- IF SEARCHED ITEM DOES NOT EXIST, SEND USER TO HOME PAGE -------
    if len(dictionary) < 5:
        error = True
        return render_template('home.html', error=error, search_term=item)

    elif r.raise_for_status() == None:
        for i in dictionary:
            key = i
            val = dictionary[key]
            if key == "href":
                href = val
            if key == "total":
                total = val
            if key == "next":
                nxt = val
            if key == "limit":
                limit = val
            if key == "itemSummaries":
                item_summary = [item for item in val]
        return render_template(render_str, total=total, limit=limit, items=item_summary, search_term=item, random=rand)

    else:
        error = True
        return render_template('home.html', error=error, search_term=item)

# ----------------------- HELPER FUNCTION FOR SEARCHING FOR A SPOTIFY TRACK -------------------------
def make_spotify_search(track):
        myparams = {'type': 'track'}
        myparams['q'] = track
        url = "https://api.spotify.com/v1/search?q=" + track + "&type=track"
        data = requests.get(url, headers=session['auth_header'])
        dictionary = data.json()
        artists = []
        for i in dictionary['tracks']['items']:
            for j in i['album']['artists']:
                artists.append(j['name'])
        if (not artists):
            return None

        return artists

if __name__ == "__main__":
    # this is invoked when in the shell  you run
    # $ python app.py
    app.run(port=8081, debug=True)
