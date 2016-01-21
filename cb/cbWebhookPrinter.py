'''
@title    cbWebhookPrinter.py

@summary: Reporting bug in coinbase server when webhook is IP address.
          (Problematic: Makes Django fail to receive checkout notifications.)

          Simple webserver with GET and POST on '/' route.
            GET creates Coinbase checkout
            POST receives notifications after payment.

@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 21 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

@requires: (1) your API_KEY, API_SECRET for your Coinbase sandbox account
           (2) upload to a digitalocean VPS droplet, example: 208.68.38.174
           (3) pip install cherrypy
           (4) python cbWebhookPrinter.py
           (5) curl -X POST -d {} -H "Content-Type: application/json" http://208.68.38.174
           (6) browser http://208.68.38.174
           (7) make payment, watch server log 
           
           --> 'Host:' header empty. Not valid according to RFC 1034/1035.   
'''

MY_URL="http://208.68.38.174"  # change to your droplet IP

from cbPersonal import API_KEY, API_SECRET 
# import coinbase sandbox credentials, or type them here:
# API_KEY, API_SECRET = "", ""

API_BACKEND_URL, API_FRONTEND_URL = ('https://api.sandbox.coinbase.com', 
                                     'https://sandbox.coinbase.com')

import cherrypy # pip install cherrypy
from coinbase.wallet.client import Client


def cbCheckoutUrl(webhook, amount=0.000101, currency="BTC"):
  """get payment URL from coinbase"""
  
  client = Client(API_KEY, API_SECRET, base_api_uri=API_BACKEND_URL)
  parameters={"amount": "%s" % amount, "currency": currency, "name": "test", 
             "notifications_url" : webhook }
  checkout = client.create_checkout(**parameters)
  embed_code=checkout["embed_code"] # print embed_code 
  payment_url='%s/checkouts/%s' % (API_FRONTEND_URL, embed_code)
  return payment_url


def test_cbCheckoutUrl(thenExit=True):
  """The tutorial suggests requestb.in; and there, the problem does NOT appear!"""
  
  WEBHOOK="http://requestb.in/17v5yh31"
  print "pay here:"
  print cbCheckoutUrl(webhook="http://requestb.in/17v5yh31")
  print "then check the results on:\n%s?inspect" % WEBHOOK
  if thenExit: exit()  


def alertText(t):
  """attention seeker"""
  print "-" * len(t), "\n", t, "\n", "-" * len(t)


def html_clickForCheckout(url):
  """put payment url into webpage, for easy clicking"""
  
  HTML= ('<html><body>Please pay on <a href="%s">%s</a> '
         'with sandbox money to trigger the callback, '
         'then watch the server log.</body></html>')
  alertText("watch this space after payment!")
  return HTML % (url, url)


def headersTable():
  """prints all headers of the request"""
  
  return "\n".join( ["%s: %s"%(K, V) 
                     for K, V in cherrypy.request.headers.items()] )


class HeaderPrinterWebService(object):
  """webserver with GET and POST, both on '/' route"""
  
  exposed = True

  def GET(self):
    payment_url = cbCheckoutUrl(webhook=MY_URL)
    return html_clickForCheckout(payment_url)

  def POST(self, length=8):
    h = headersTable()
    alertText("These are the headers of the incoming POST request. Check out 'Host:'")
    print h
    return h  # curl -X POST -d {} -H "Content-Type: application/json" http://208.68.38.174

  
if __name__ == '__main__':
  
  # test_cbCheckoutUrl(thenExit=True)
 
  conf = {
      '/': {
          'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
      },
      'global':    { 'server.socket_host': '0.0.0.0',
                     'server.socket_port': 80,
                    }
  }
  service = HeaderPrinterWebService()
  cherrypy.quickstart(service, '/', conf)
