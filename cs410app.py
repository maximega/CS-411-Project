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
a_t = "v^1.1#i^1#r^0#p^1#f^0#I^3#t^H4sIAAAAAAAAAOVXa2wUVRTuttsSLEUlgICQrFMNz5mdmZ3dnRnZDUsLdBOgK1taKWC5O3OnHTs7M86dpV3EWJeESIIRjI+YGKmJqMXwMoqYoCIJikTjAwyIPHwkPiKJ/jDhESTemS5lWwlQWITE/bO555577vd955x759JdFUOnrK5bfarKM6S0u4vuKvV4mEp6aEX51OFlpePKS+gCB093171d3lzZr9MRSGumuAAi09AR9HWmNR2JrjFCZCxdNABSkaiDNESiLYnJ2Ly5IkvRomkZtiEZGuGL10YIHvJKgOMkEBSElCKx2KpfiNlgRAhFkQSFlRmG5yGXgngaoQyM68gGuh0hWJrhSYYhaaGBCYssL3I8xQlcM+FrhBZSDR27UDQRddGK7lqrAOrlkQKEoGXjIEQ0HpudrI/Fa2fNb5juL4gVzcuQtIGdQf1HNYYMfY1Ay8DLb4NcbzGZkSSIEOGP9u7QP6gYuwDmGuC7SiuhAC1xENKKAPgAGyqKlLMNKw3sy+NwLKpMKq6rCHVbtbNXUhSrkXoYSnZ+NB+HiNf6nL8HMkBTFRVaEWLWzNiiWCJBROeBTjUN5wCyVVXsVnU5JBMLaklBYtkUz4YByaRACHIsk9+oN1pe5gE71Ri6rDqiId98w54JMWo4UBumQBvsVK/XWzHFdhAV+gkXNOSFZiepvVnM2G26k1eYxkL43OGVM9C32rYtNZWxYV+EgROuRBECmKYqEwMn3VrMl08nihBttm2Kfn9HRwfVEaAMq9XP0jTjf3De3KTUBtOAcHydXnf91SsvIFWXioTbFPuLdtbEWDpxrWIAeisRDXA0Iwh53fvDig60/stQwNnfvyOK1SEgSIchLckcT+NeYflidEg0X6R+BwdMgSyZBlY7tE0NSJCUcJ1l0tBSZTEQVNgAr0BSDgkKyQmKQqaCcohkFNyyEKZSksD/nxrlaks9KRkmTBiaKmWLU/BFK3ZLTgDLziahpmHD1Vb9JUkih+SNp+f0+mAoOjEQDgJMlXJqm5KMtN8A+FBzTC0u6uviHTPNeDqdsUFKg/EiHWg35zC7JD0VX/e3FCecv95EqnLvPU252aTQcomyIDIyFv5Eoeqda6vBaIc6PgRsy9A0aDUy153oWyy/gzwrr413ES/qQfLGvc7cyNqWNBWXUMtNYndzs6oC+9ZizQQ5JsxzQZa/Ll41bk4bsv/FXTQYenUGsqF8A74r/f0fudES98fkPO/QOc92/E6m/fR9TDV9T0XZQm/ZsHFItSGlAoVCaquOH28WpNph1gSqVVrhWTx+W09LwbO6eyk9pu9hPbSMqSx4ZdPjL86UM7ffVcXwDEMLTJjlOb6Zrr4462VGe0cu8Yw9v4LQfvnit9c/Orvn1RenHTw0hq7qc/J4yku8OU9J1Nd9x2dHT5xZpox8bcc3o6vWLplRvfHE0WfAD8TqGQfDX25+qXybeGqK/N3Gr3qaE+NWHpr48uN/5pZ+exz83vL2ibb9Ryavq9h35v7bnh81oWfL9nc3Tas/eeDs1IU1n+Q2rUezNjSG0kPmtuwcBps2fb2Fyx4/0HL68OeH54Q37B7xZDT4wcJR2v59O/5es+/IzyNON/3kHaUN73zKPDd7T+Wqk9E/0ApvavJW5tiKpuAT/HufTqrr3rxr96qdB9dbW7bufSTR8FD78je2nVubvXuCbwqof+z8c+OPjZz0V+ULcfrOmYvXLKrukVf6f9yxa3/tsu9z2ivrHq1ufmui8eyHxyN7x4be3/vx0282ra/rTd8/yhyyfPAQAAA="


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/result', methods=['GET'])
def result():
    iden = request.args.get('search')
    #if (iden == "maxime gavronsky" or iden == "Maxime Gavronsky"):
    place_holder = "me"
    #add ebay headers 
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
