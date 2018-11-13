import tweepy
import socket
import json
import sys
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

host = "localhost"    # Get local machine name
port = 5555           # Reserve a port for streaming.

class TweetsListener(StreamListener):
    def __init__(self, csocket):
        self.client_socket = csocket

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            print(tweet['text'])
            self.client_socket.send(tweet['text'].encode('utf-8'))
            # return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)
        return False

def sendData(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=[sys.argv[1]])


# s: socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port)) # Bind to the port
    print("Listening on port: %s" % str(port))

    s.listen(1) # Now wait for 1 client connection.
    conn, addr = s.accept() # Establish connection with client.
    with conn:
        print('Received request from:', addr)
        while True:
            sendData(conn)
        print('Connection lost with:', addr)
