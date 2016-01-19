'''
@title    cbCheckout.py
  
@summary  play with coinbase API: Checkouts
          with resulting callback data sent to webhook, e.g. requestb.in
  
  
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 19 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''

WEBHOOK_URL="http://requestb.in/w2vw66w2"


from cbPersonal import API_KEY, API_SECRET, PRODUCTION

SANDBOX_URLS = ('https://api.sandbox.coinbase.com', 'https://sandbox.coinbase.com')
PRODUCTION_URLS=(      'https://api.coinbase.com' , 'https://coinbase.com')
API_BACKEND_URL, API_FRONTEND_URL=PRODUCTION_URLS if PRODUCTION else SANDBOX_URLS 

from coinbase.wallet.client import Client


def createCheckoutCallback(amount=0.000101, currency="BTC",
                           metadata={"test": 42}, 
                           hook=WEBHOOK_URL):
  
  client = Client(API_KEY, API_SECRET, base_api_uri=API_BACKEND_URL)

  parameters={ "amount": "%s" % amount,
             "currency": currency,
             "name": "test",
             "type": "order",
             "style": "buy_now_large",
             "customer_defined_amount": "false",
             "collect_email": "false",
             "metadata": metadata,
             "notifications_url" : hook     
             }
  
  checkout = client.create_checkout(**parameters)
  
  embed_code=checkout["embed_code"]
  print embed_code 
      
  payment_url='%s/checkouts/%s' % (API_FRONTEND_URL, embed_code)
  print payment_url


def test_createCheckoutCallback():
  createCheckoutCallback()
  

if __name__ == "__main__":
  test_createCheckoutCallback()
  