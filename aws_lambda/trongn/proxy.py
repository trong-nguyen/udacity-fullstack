import os
import json
import urllib
from base64 import b64encode

# external libs
import requests

class Proxy(object):
    URL          = None
    ACCESS_TOKEN = None

    def __init__(self):
        super(Proxy, self).__init__()

    def build_query(self, params):
        return urllib.urlencode(params)

    def build_headers(self):
        return {
            'Content-Type': 'application/json',
        }

    def get_url(self):
        return self.URL

    def fetch(self, params):
        response = requests.get(
            url     = '?'.join([self.get_url(), self.build_query(params)]),
            headers = self.build_headers()
        )

        return response

class YelpProxy(Proxy):
    URL = 'https://api.yelp.com/v3/businesses/search'

    def get_access_token(self):
        '''
        Use environment credentials to obtain access token
        Tokens are cached so it takes only one request
        '''
        if not self.ACCESS_TOKEN:
            url = 'https://api.yelp.com/oauth2/token'

            params = {
                'grant_type'    : 'client_credentials',
                'client_id'     : os.environ['YELP_CLIENT_ID'],
                'client_secret' : os.environ['YELP_CLIENT_SECRET']
            }

            response = requests.post(url, params=params)
            message = response.json()
            self.ACCESS_TOKEN = message['access_token']

        return self.ACCESS_TOKEN

    def build_headers(self):
        headers = super(YelpProxy, self).build_headers()
        access_token = self.get_access_token()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token)
            })

        return headers

class TwitterProxy(Proxy):
    URL = 'https://api.twitter.com/1.1/search/tweets.json'

    def get_access_token(self):
        if not self.ACCESS_TOKEN:
            url = 'https://api.twitter.com/oauth2/token'

            credentials = b64encode(':'.join([
                    os.environ['TWITTER_CONSUMER_KEY'],
                    os.environ['TWITTER_CONSUMER_SECRET']
                    ]))

            headers = {
                'Authorization': 'Basic ' + credentials,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }

            params = {
                'grant_type': 'client_credentials'
            }

            response = requests.post(url, params=params, headers=headers)
            message = response.json()
            self.ACCESS_TOKEN = message['access_token']

        return self.ACCESS_TOKEN

    def build_headers(self):
        headers = super(TwitterProxy, self).build_headers()
        access_token = self.get_access_token()
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token)
            })

        return headers

class FoursquareProxy(Proxy):
    URL = 'https://api.foursquare.com/v2/venues/search'

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
        response_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

        try:
            params = event['queryStringParameters']
            r = fetcher.fetch(params)

            return {
                'statusCode' : r.status_code,
                'body'       : r.content,
                'headers'    : response_headers
            }

        except:
            return {
                'statusCode' : '400',
                'body'       : 'Exception thrown while fetching data',
                'headers'    : response_headers
            }

    return handler

def make_proxy_handler(name):
    proxy = None

    available_proxies = {
        'Twitter'    : TwitterProxy,
        'Foursquare' : FoursquareProxy,
        'Yelp'       : YelpProxy
    }

    try:
        proxy = available_proxies[name]
    except KeyError as e:
        raise ValueError('Invalid proxy: {}'.format(name))

    return base_handler(proxy)
