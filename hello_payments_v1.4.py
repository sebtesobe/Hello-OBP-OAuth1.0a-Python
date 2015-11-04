# -*- coding: utf-8 -*-

import json
import sys
from pprint import pprint

from oauth_dance import get_api
from settings import (
    API_HOST, OUR_BANK, COUNTERPART_BANK, COUNTERPART_ACCOUNT_ID)


api_base_url = '{}/obp/v1.4.0'.format(API_HOST)
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

print('Get challenge request types: ')
response = openbank.get('{}/transaction-request-types'.format(api_owner_url))
challenge_type = response.json()[0]['value']
print(challenge_type)


print("Initiate transaction request:")
headers = {'content-type': 'application/json'}

uri = '{}/transaction-request-types/sandbox/transaction-requests'
url = uri.format(api_owner_url)
body = json.dumps({
    'to': {
        'account_id': COUNTERPART_ACCOUNT_ID,
        'bank_id': COUNTERPART_BANK,
    },
    'value': {
        'currency': 'GBP',
        'amount': '1'
    },
    'description': 'Description abc',
    'challenge_type': challenge_type,
})
response = openbank.post(url, data=body, headers=headers)
request_response = response.json()
if 'error' in request_response:
    print(request_response['error'])
    sys.exit(2)
challenge_id = request_response['challenge']['id']
print('Challenge id is {}'.format(challenge_id))

transaction_id = request_response['id']['value']
print('Transaction id is {}'.format(transaction_id))
uri = '{}/transaction-request-types/sandbox/transaction-requests/{}/challenge'
url = uri.format(api_owner_url, transaction_id)
body = json.dumps({
    'id': challenge_id,
    'answer': '123456',  # any number works in sandbox mode
})
response = openbank.post(url, data=body, headers=headers)
challenge_response = response.json()
if 'error' in challenge_response:
    print(challenge_response['error'])
    sys.exit(3)
print('Transaction status: {}'.format(challenge_response['status']))
