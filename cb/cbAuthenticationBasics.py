'''
@title      cbAuthenticationBasics.py
  
@purpose    play with coinbase API: Requests how to. 
  
@summary    Trying out the tutorial on https://developers.coinbase.com  --> Python
          
            Looking behind the curtains of the ready-made Python Library:
            --> Create custom authentication for Coinbase API
          
            Understand how the communication with the server is initiated:
            https://developers.coinbase.com/docs/wallet/api-key-authentication#making-a-request
            
            Comes in handy when the official Python library has a bug,
            e.g. see cbNotificationsBug.py 
  
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 11 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''

from cbPersonal import API_KEY, API_SECRET, EMAILADDRESS2, API_BACKEND_URL
from cbWallet import random2Digits

print API_BACKEND_URL

from pprint import pprint
import hmac, hashlib, time

# pip install requests
import requests


def requestResultPrinter(r, headers=True):
  """Perhaps prints headers, then important attributes of request r"""
  if headers:
    print "headers:", 
    pprint (dict(r.headers))
  for attrib in ["status_code", "reason", "elapsed", "url", "encoding"]:
    print attrib, ":", r.__dict__[attrib]


def moneyFormat(money):
  """200.12 EUR, or 0.00001500 BTC"""
  return "%s %s" % (money["amount"], money["currency"])


class CoinbaseWalletAuth(requests.auth.AuthBase):
  """
  Authenticate at coinbase server. 
  """
  
  def __init__(self, api_key, secret_key, API_BACKEND_URL):
    """store credentials for later"""
    self.api_key = api_key
    self.secret_key = secret_key
    self.API_BACKEND_URL = API_BACKEND_URL # + "/v2/" 

  def __call__(self, request):
    """signed message, with correct headers."""
    # prepare message to be signed
    timestamp = str(int(time.time()))
    message = timestamp + request.method + request.path_url + (request.body or '')
    
    # sign it:
    signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
  
    # set headers
    request.headers.update({
        'CB-ACCESS-SIGN': signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': self.api_key,
        'CB-VERSION' : "2016-01-13"      # see https://developers.coinbase.com/api/v2#versioning
    })
    return request


  def getCurrentUser(self):
    """The user, with id, name, country, email, etc."""
    return requests.get(self.API_BACKEND_URL + '/v2/user', auth=self)
    
  def printCurrentUser(self):
    print"\nGet current user:"
    r=self.getCurrentUser()
    pprint ( r.json() )
    return r
      
      
  def sendFunds(self):
    print "\nSend funds:"
    tx = {
        'type': 'send',
        'to': EMAILADDRESS2,
        'amount': '0.%s' % random2Digits(),
        'currency': 'THB',
    }
    r = requests.post(self.API_BACKEND_URL + '/v2/accounts/primary/transactions', 
                      json=tx, auth=self,
                      # "important that your application validates our SSL certificate:"
                      verify=True )  # True is default anyways. False results in Warning.
    # print dir (r)
    print "Request posted, this is the result:\n"
    requestResultPrinter(r)
    print "\nText:", 
    pprint ( r.json() )
    return r
  

  def checkOptionsVerb(self):
    print "\nChecking if the OPTIONS verb is implemented."
    r = requests.options(self.API_BACKEND_URL)
    requestResultPrinter(r, headers=False)
    if r.status_code == requests.codes.ok:
      print r.json()
      

def test_CoinbaseWalletAuth():

  auth = CoinbaseWalletAuth(API_KEY, API_SECRET, API_BACKEND_URL)

  auth.printCurrentUser()
  
  auth.sendFunds()
  
  auth.checkOptionsVerb()
  

if __name__ == "__main__":
    
  test_CoinbaseWalletAuth()
  
  