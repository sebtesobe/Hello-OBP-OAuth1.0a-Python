# -*- coding: utf-8 -*-

import json
import sys
from pprint import pprint

from oauth_dance import get_api
from settings import (
    API_HOST, OUR_BANK, COUNTERPART_BANK, COUNTERPART_ACCOUNT_ID)


api_base_url = '{}/obp/v1.2.1'.format(API_HOST)
api_accounts_url = '{}/banks/{}/accounts'.format(api_base_url, OUR_BANK)
openbank = get_api()

# get accounts for a specific bank
print('Available private accounts:')
response = openbank.get('{}/private'.format(api_accounts_url))
response_json = response.json()
pprint(response_json)
accounts = response_json['accounts']
if len(accounts) < 1:
    print('No private accounts found, exiting...')
    sys.exit(1)

# just picking first account
our_account = accounts[0]['id']
print('Our account: {} ({})'.format(our_account, accounts[0]['label']))
api_owner_url = '{}/{}/owner'.format(api_accounts_url, our_account)

print('Get owner transactions: ')
response = openbank.get(
    '{}/transactions'.format(api_owner_url),
    headers={'obp_limit': '25'},
)
transactions = response.json()['transactions']
print('Got {} transactions'.format(len(transactions)))


print('Transfer some money: ')
headers = {'content-type': 'application/json'}
body = json.dumps({
    'account_id': COUNTERPART_ACCOUNT_ID,
    'bank_id': COUNTERPART_BANK,
    'amount': '1',
})
response = openbank.post(
    '{}/transactions'.format(api_owner_url), data=body, headers=headers)
print(response)
print(response.json())
