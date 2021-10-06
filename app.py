from json import loads
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from tweets import Tweets
from requests.sessions import Session
import json
import tweets
from flask import request
import flask

app = Flask(__name__)


def get_videos(channelid, maxResults, key, part,):
    url = "https://youtube.googleapis.com/youtube/v3/playlists"
    parameters = {
        "channelId": channelid,
        "maxResults": maxResults,
        "key": key,
        "part": part
    }

    headers = {
        'Accept': 'Application/json',
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    return response


@app.route('/', methods=['POST'])
def search():
    search = request.form.get("search")
    tweet = Tweets(search)
    tweetdata = tweet.get_tweet()
    tweetdict = tweetdata.to_dict(orient='records')
    return render_template('index.html', tweetdata=tweetdict)


@app.route('/', methods=['POST'])
def tweet():
    tweet = Tweets("microsoft")
    tweetdata = tweet.get_tweet()
    tweetdict = tweetdata.to_dict(orient='records')
    return render_template('tweets.html', tweetdata=tweetdict)


@app.route('/', methods=['GET', 'POST'])
def index():
    tweet = Tweets("microsoft")
    tweetdata = tweet.get_tweet()
    tweetdict = tweetdata.to_dict(orient='records')
    response = render_template(
        'index.html', tweetdata=tweetdict)
    return response


if __name__ == "__main__":
    app.run(debug=True)
