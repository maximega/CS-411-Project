import flask
from flask import Flask, Response, request, render_template, redirect, url_for
import requests
#from flaskext.mysql import MySQL
#import flask.ext.login as flask_login
#import re

# for image uploading
# from werkzeug import secure_filename
#import os
#import base64

app = Flask(__name__)
a_t = insert_key_here


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/result', methods=['GET'])
def result():
    iden = request.args.get('search')
    #if (iden == "maxime gavronsky" or iden == "Maxime Gavronsky"):
    place_holder = "me"
    res = "https://graph.facebook.com/v3.2/" + place_holder + "?fields=id,name,email,last_name,likes&access_token=" + a_t
    call = requests.get(res)
    call.raise_for_status()
    dictionary = call.json()
    s = ""
    for i in dictionary:
        if i == "likes":
            s += i + ":"
            for j in dictionary[i]:
                if j == "data":
                    s += "\n\t" + j + ":\n"
                    for k in dictionary[i][j]:
                        dictk = k
                        for l in dictk:
                            if (l == "cursor"):
                                continue
                            s+= "\n\t\t"
                            s+= l
                            s+= ":\t"
                            s+= dictk[l]
                            s+=  "\n"
        else:
            s += "\n" + i + ":\t" + dictionary[i] + "\n"
    print(s)
    return s
