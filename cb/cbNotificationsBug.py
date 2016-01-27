'''
@title    cbNotificationsBug.py
  
@purpose  examine the .get_notifications() bug
                      TypeError: unhashable type: 'dict'     
  
@summary  Trying out the tutorial on   
          https://developers.coinbase.com/docs/wallet/notifications --> Python 
          
          .get_notifications() from the official Python library has a bug.
          
          So I am downloading that data which causes the TypeError,
          using a manually constructed CoinbaseWalletAuth.
          
  
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 11 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''

from cbPersonal import API_KEY, API_SECRET, API_BACKEND_URL
import cbAuthenticationBasics

import traceback, sys
import requests # pip install requests
  
bug_account_IDs=["0a30666a-33a5-5685-a81f-69be194d8602", 
                 "8a7b0da0-ff92-5cb6-b42c-2b0d5c26e438"]
  
def BUG_get_notifications():
  print "\n'client.get_notifications()' is ill somehow!", 
  print "  TypeError: unhashable type: 'dict'"
  print "(with some accounts, e.g. %s)\n" % bug_account_IDs

  try:
    
    
    from coinbase.wallet.client import Client # here is the problem:  
    notifications = Client(API_KEY, API_SECRET, API_BACKEND_URL).get_notifications()
    
    
    print notifications.keys()
  except Exception as e:  
    print "exception caught: ", type(e), e
    
    for frame in traceback.extract_tb(sys.exc_info()[2]):
      fname,lineno,fn,text = frame
      print "%s [in %s] line %d of %s" % (text, fn, lineno, fname)
        
    

class myOwnAuth(cbAuthenticationBasics.CoinbaseWalletAuth):
  """see cbAuthenticationBasics for more info"""
  
  def get_notifications(self):
    print"\nGetting ALL notifications:"
    url=self.API_BACKEND_URL + '/v2/notifications'
    return requests.get(url, auth=self)
    
  def get_and_show_notifications(self, notifId=""):
    r = self.get_notifications()
    cbAuthenticationBasics.requestResultPrinter(r, headers=False)
    if r.status_code == requests.codes.ok:
      print "text:\n%s" % r.text
    return r
    

if __name__ == "__main__":
  
  ###### this causes a bug (for my account that is) 
  BUG_get_notifications()
  ######
  
  print "\nCoinbase.wallet.client.Client().get_notifications()", 
  print "is failing with a TypeError.\nTrying to find out the reasons,",
  print "by using my own auth-library ... This is the provoking data:\n"
  
  auth = myOwnAuth(API_KEY, API_SECRET, API_BACKEND_URL)
  user=auth.getCurrentUser().json()["data"]
  print "Authentication succeeded, user='%s'" % user["id"]
  
  r=auth.get_and_show_notifications()
  
