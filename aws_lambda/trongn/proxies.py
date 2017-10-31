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

class Proxy(object):
    def __init__(self):
        super(Proxy, self).__init__()

    def build_query(self, params):
        return urllib.urlencode(params)

    def build_headers(self):
        return {
            'Content-Type': 'application/json',
        }

    def fetch(self, params):
        response = requests.get(
            url     = self.URL + self.build_query(params),
            headers = self.build_headers()
        )

        return response.content

class TweeterProxy(Proxy):
    URL = 'https://api.twitter.com/1.1/search/tweets.json?'

    def build_headers(self):
        headers = super(TweeterProxy, self).build_headers()
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token)
            })

        return headers

class FoursquareProxy(Proxy):
    URL = 'https://api.foursquare.com/v2/venues/search?'

    def build_query(self, params):
        params = dict(params)

        auth = {
            'client_id'     : os.environ['FOURSQUARE_CLIENT_ID'],
            'client_secret' : os.environ['FOURSQUARE_CLIENT_SECRET'],
            'v'             : '20170801'
        }

        params.update(auth)

        return super(FoursquareProxy, self).build_query(params)


def base_handler(proxy):
    '''
    A simple catch - adding auth - request and return kind of proxy server
    The handle forward the entire query string to 3rd party API
    only adding authentication credentials if neccessary
    '''
    fetcher = proxy()

    # depending on wheather proxy integration is used
    # data should be in serialized or plain dict form
    # status code, headers and body mus be present in the response
    def handler(event, context):
        params = event['queryStringParameters']
        data = fetcher.fetch(params)
        return respond(None, data)

    return handler