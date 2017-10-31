import os
import json
import urllib

# external libs
import requests

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

def fetch_tweets(query_string):
    url = 'https://api.twitter.com/1.1/search/tweets.json?'
    access_token = os.environ['TWITTER_ACCESS_TOKEN']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }

    response = requests.get(url + query_string, headers=headers)

    return response.content


def handler(event, context):
    '''
    A simple catch - adding auth - request and return kind of proxy server
    The handle forward the entire query string to 3rd party API
    only adding authentication credentials if neccessary
    '''

    query_string = urllib.urlencode(event['queryStringParameters']);
    data = fetch_tweets(query_string)

    # depending on wheather proxy integration is used
    # data should be in serialized or plain dict form
    # status code, headers and body mus be present in the response
    return respond(None, data)