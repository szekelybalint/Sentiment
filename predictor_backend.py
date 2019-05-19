import flask
from flask_cors import CORS
import pandas as pd
import tensorflow as tf
import keras
import joblib
from keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Thread
import json
import tweet_cleaner
 
import twitter_credentials


app = flask.Flask(__name__)

global graph
graph = tf.get_default_graph()

model = load_model('C:/Projects/Sentiment/second.h5')
vectorizer = joblib.load('vectorizer.pkl')


positives = []
negatives = []


# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}

    params = flask.request.json
    x = params['text']
    with graph.as_default():
        data["prediction"] = str(model.predict_classes(vectorizer.transform([x]))[0][0])
        data["success"] = True

    # return a response in json format 
    return flask.jsonify(data)    


@app.route("/positive_tweets", methods=["GET"])
def positive_tweets():

    # return a response in json format 
    return flask.jsonify(positives)    

@app.route("/negative_tweets", methods=["GET"])
def negative_tweets():

    # return a response in json format 
    return flask.jsonify(negatives)    

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            # print(json_data['text'])
            # clean
            cleaned = tweet_cleaner.tweet_cleaner(json_data['text'])
            prediction = str(model.predict_classes(vectorizer.transform([cleaned]))[0][0])
            if (prediction == '1'):
                positives.append(cleaned)
            else:
                negatives.append(cleaned)
            # print(cleaned + '\n predicted value: ' +prediction)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()
        print('twitter streamer')  

    def stream_tweets(self, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener()
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list,languages=["en"])

    def run(self):
        hash_tag_list = ["Game of thrones", "GameOfThrones"]
        print('starting twitter stream')
        t = Thread(target=self.stream_tweets(hash_tag_list))
        t.setDaemon(True)
        t.start()


def flask_thread():
    CORS(app)
    app.run()


if __name__ == '__main__':


    ts = TwitterStreamer()
    Thread(target=flask_thread).start()
    ts.run()

