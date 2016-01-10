'''
@title    cbSendRequest.py
  
@purpose  several errors on tutorial page:
  
@summary  https://developers.coinbase.com/docs/wallet/guides/send-receive
          --> Python 
          'send funds' on that page is wrong.
          'request funds' on that page is wrong
  
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 10 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''

# API authorization for sandbox. Import, or define here manually.
from cbPersonal import API_KEY, API_SECRET

# N.B.: Needs email address of a 2nd coinbase 'sign up' account, 
# to request money from. Because I cannot 'request_money' from myself.
from cbPersonal import EMAILADDRESS2  

from cbWallet import pause

def connectAndGetPrimaryAccount():
  from coinbase.wallet.client import Client

  SANDBOX_URL = 'https://api.sandbox.coinbase.com'
  client = Client(API_KEY, API_SECRET,
                  base_api_uri=SANDBOX_URL)

  print "\nGet your primary coinbase account:", 
  primary_account = client.get_primary_account()
  print type(primary_account), primary_account["id"]
  
  return primary_account


def sending(primary_account):
  print "\nCreate Bitcoin address in that account:"
  address = primary_account.create_address()
  print type(address), address.address
  print address
  
  try:
    print "\nprimary_account.send_money like said in tutorial:"
    tx = primary_account.send_money({'to': address, 'amount': '0.01', 'currency': 'BTC'})
  except Exception as e:
    print "exception caught: ", type(e), e
    print "Syntax given in tutorial, with dictionary of arguments, is wrong."
    
  try:
    print "\nprimary_account.send_money(to=address.address ..."
    tx=primary_account.send_money(to=address.address, amount='0.01', currency='BTC')
    print tx
  except Exception as e:
    print "exception caught: ", type(e), e
    print "So this tutorial sentence is also wrong: ",
    print "'(since it is your own address, the funds will just come back to your primary wallet)'" 


def requesting(primary_account):
    
  print "\nrequest money:"
  try:
    print "\nprimary_account.request_money ... like said in tutorial:" 
    tx = primary_account.request_money({'to': EMAILADDRESS2,'amount': '0.1','currency': 'BTC'})
    print tx
  except Exception as e:
    print "exception caught: ", type(e), e
    print "Syntax given in tutorial, with dictionary of arguments, is wrong."
    
  print "\nThis does work:"
  print "primary_account.request_money(to=....@....,amount='0.01',currency='BTC')"
  tx=primary_account.request_money(to=EMAILADDRESS2,amount='0.01',currency='BTC', 
              description='Cannot request money from myself, so testing from another account.')
  print tx
  
  
  print "\nThis tx has gone through, and looks fine."
  print "BUT: never leaves 'status=pending'. And no email is arriving!"

def errorsInTheTutorial():

  primary_account = connectAndGetPrimaryAccount()
  
  sending(primary_account)
    
  pause()
  
  requesting(primary_account)


if __name__ == "__main__":
  
  errorsInTheTutorial()

  

