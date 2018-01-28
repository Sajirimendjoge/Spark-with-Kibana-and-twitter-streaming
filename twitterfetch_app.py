import socket
import sys
import json
import requests
import requests_oauthlib

# Replace the values below with your relevant TWITTER Credentials
ACCESS_TOKEN = '2588737064-Rrf6bipN6ScsQKa0PLJNdItgYKecw0hiOS9RycG'
ACCESS_SECRET = 'pYgU0ofmaVAefXgG8taK04T9JMv0KRKNXvjbtPMGDH4Sv'
CONSUMER_KEY = 'rFu2LTWV4fgxiIsLIS4rkIrn9'
CONSUMER_SECRET = 'SClUZ8dnmMK12LifCReZEcEZwBgL7R4QpuIT3fHVV0VE7VCu7S'
TCP_IP = "localhost"
TCP_PORT = 9009

def send_tweets_spark(http_resp, tcp_connection):
    '''
    The function receives TCP connection and reponse as parameters
    and loads current tweets through TWITTER API and send to Spark.

    Args:
        http_resp (object) : It is a http respnose which is returning tweets.
        tcp_connection (object) : TCP socket connection object

    Returns:
        None
    '''
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            print("Tweet Text: " + tweet_text)
            print("~" * 40) # to print a line as seperator
            tcp_connection.send(tweet_text.encode('utf-8'))
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)

def get_twitter_tweets():
    '''
    The function queries for data from currently running tweets from Twitter API and
    print the respective url

    Returns:
        object : http response object after getting tweets from twitter API
    '''
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    query_data = [
        ('language', 'en'),
        ('locations', '-122.75,36.8,-121.75,37.8,-74,40,-73,41'),
        ('track', '#')
    ]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=user_auth, stream=True)
    print(query_url, response)
    return response

if __name__ == '__main__':
    user_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection to open...")
    conn, addr = s.accept()
    print("Connected... Tweets are getting started.")
    resp = get_twitter_tweets()
    send_tweets_spark(resp, conn)
