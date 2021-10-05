from json import loads
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from tweets import Tweets
from requests.sessions import Session
import json
import tweets
from flask import request

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
def tweet():
    data = get_videos("UCoG2o8WtvYh8sCS40pUFtCg", 25,
                      "AIzaSyDwfhqAFIS2-H8lboqAyOd0zAT2Jazuf24", "snippet")
    response = json.loads(data.text)

    def search():
        search = request.form.get('search')
        return search
    tweet = Tweets(search)
    tweetdata = tweet.get_tweet()
    tweetdict = tweetdata.to_dict(orient='records')
    return render_template('tweets.html', response=response, tweetdata=tweetdict)


@app.route('/', methods=['GET', 'POST'])
def index():
    data = get_videos("UCoG2o8WtvYh8sCS40pUFtCg", 25,
                      "AIzaSyDwfhqAFIS2-H8lboqAyOd0zAT2Jazuf24", "snippet")
    response = json.loads(data.text)

    def search():
        search = request.form.get('search')
        return search
    tweet = Tweets("microsoft")
    tweetdata = tweet.get_tweet()
    tweetdict = tweetdata.to_dict(orient='records')
    return render_template('index.html', response=response, tweetdata=tweetdict)


if __name__ == "__main__":
    app.run(debug=True)
