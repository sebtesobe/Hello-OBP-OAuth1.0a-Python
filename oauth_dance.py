# -*- coding: utf-8 -*-
# oauth flow in simple words: http://pyoauth.readthedocs.org/en/latest/guides/oauth1.html

from requests_oauthlib import OAuth1Session
from six.moves import input

from settings import CLIENT_KEY, CLIENT_SECRET, API_HOST


def get_api():
    request_token_url = '{}/oauth/initiate'.format(API_HOST)
    authorization_base_url = '{}/oauth/authorize'.format(API_HOST)
    access_token_url = '{}/oauth/token'.format(API_HOST)
    callback_uri = 'http://127.0.0.1/cb'  # can be pretty random in this case

    # initiate Oauth by fetching request token
    api = OAuth1Session(
        CLIENT_KEY, client_secret=CLIENT_SECRET, callback_uri=callback_uri)
    api.fetch_request_token(request_token_url)

    # ask user to visit authorization URL and paste response
    authorization_url = api.authorization_url(authorization_base_url)
    print('Please go here and authorize: ')
    print(authorization_url)
    redirect_response = input('Paste the full redirect URL here: ')

    # parse authorization response (contains callback_uri) and access token
    api.parse_authorization_response(redirect_response)
    api.fetch_access_token(access_token_url)
    return api
