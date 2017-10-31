import requests
import json


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def fetch_tweets(query, lat, lng, radius):
    url = 'https://api.twitter.com/1.1/search/tweets.json?'
    access_token = (
        'AAAAAAAAAAAAAAAAAAAAACXh2wAAAAAAKnNMrhBLJYhb5pC1aHWq3rbIPvc%'
        '3DmygjYj9WtadxcKbVceo9pnzLB3ZFLRL4VuGcGeVVrPaDQcJyBG'
        )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    params = {
        'q'       : query,
        'geocode' : '{},{},{}'.format(lat, lng, radius)
    }

    response = requests.get(url, params=params, headers=headers)

    return response.json()


def handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''

    data = fetch_tweets(
        query  = 'Luke\'s Lobster',
        lat    = 41.874882,
        lng    = -87.642227,
        radius = '5mi'
        )

    return respond(None, json.dumps(data))


# if __name__ == '__main__':
#     print(handler(0,0))