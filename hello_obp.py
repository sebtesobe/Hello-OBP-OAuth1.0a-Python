# -*- coding: utf-8 -*-

from oauth_dance import get_api
from settings import API_HOST

api_base_url = '{}/obp/v1.2.1'.format(API_HOST)

openbank = get_api()
response = openbank.get('{}/banks'.format(api_base_url))
print(response)
print(response.json())
