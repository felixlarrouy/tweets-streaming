import tweepy
import socket
import json
import sys
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = '8bwa6ory4xsBzOIJ2gAO2ukK2'
consumer_secret = 'cEDvbXAa9DkLPWxutnTZpF2gptgruRRj3KhGMfkYdMqkqCfdqj'
access_token = '1059729535053295617-SgThBTq7GRhA8bvqVxwatOBku3COBA'
access_token_secret = '3F6qTH4Avtqus6HowNKZHE1epGtzPPtMAk7IRhFE20HyN'

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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # socket object
    s.bind((host, port)) # Bind to the port
    print("Listening on port: %s" % str(port))

    s.listen(1) # Now wait for 1 client connection.
    conn, addr = s.accept() # Establish connection with client.
    with conn:
        print('Received request from:', addr)
        while True:
            sendData(conn)
        print('Connection lost with:', addr)
