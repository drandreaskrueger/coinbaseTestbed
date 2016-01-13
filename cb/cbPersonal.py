'''
Created on 10 Jan 2016

@author: Andreas

@summary: API keys & secrets & emailaddress2 (to request money from)

@attention: 
https://developers.coinbase.com/docs/wallet/api-key-authentication#security-best-practices

'''

# fill in your credentials:

API_KEY=""
API_SECRET=""

# Email address of a 2nd coinbase 'sign up' account, to request money from. 
# Cause I cannot 'request_money' from myself.
EMAILADDRESS2=""

PRODUCTION = False

try:
  from cbPersonal_ME import API_KEY, API_SECRET, EMAILADDRESS, EMAILADDRESS2, PRODUCTION
except:
  pass
else: 
  print "Credentials from 'cbPersonal_ME.py' which is in .gitignore. Still, better think about more security!" 

SANDBOX_URL = 'https://api.sandbox.coinbase.com'
PRODUCTION_URL=       'https://api.coinbase.com'
API_URL=PRODUCTION_URL if PRODUCTION else SANDBOX_URL 
