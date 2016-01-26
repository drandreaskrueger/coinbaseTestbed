'''
@title    cbWebhookPrinter.py

@summary: Reporting bug in coinbase server if webhook is an IP address.

          Problematic: Makes Django fail to receive checkout notifications.
          See 'HOST-header_empty.md' for details. 

          This is a:
                     Simple cherrypy webserver with GET and POST on '/' route.
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
           (5) browser http://208.68.38.174
           (6) curl -X POST -d {} -H "Content-Type: application/json" http://208.68.38.174/hook
           (7) reload iframe
           (8) make payment, reload iframe
           
           --> Coinbase notification:
                'Host:' header empty. Not valid according to RFC 1034/1035.   
'''

VERSION=   "v0.06"

MY_URL="http://208.68.38.174"  # change to your droplet IP

from cbPersonal import API_KEY, API_SECRET 
# import coinbase sandbox credentials, or type them here:
# API_KEY, API_SECRET = "", ""

API_BACKEND_URL, API_FRONTEND_URL = ('https://api.sandbox.coinbase.com', 
                                     'https://sandbox.coinbase.com')

import cherrypy # pip install cherrypy
import pprint, json
from coinbase.wallet.client import Client


def cbCheckoutUrl(webhook, amount="0.000101", currency="BTC", dbg=True):
  """get payment URL from coinbase"""
  
  client = Client(API_KEY, API_SECRET, base_api_uri=API_BACKEND_URL)
  parameters={"amount": amount, "currency": currency, "name": "test", 
             "notifications_url" : webhook }
  checkout = client.create_checkout(**parameters)
  embed_code=checkout["embed_code"] # print embed_code 
  payment_url='%s/checkouts/%s' % (API_FRONTEND_URL, embed_code)
  if dbg: print "checkout created, with notifications_url=%s" % webhook
  return payment_url


def test_cbCheckoutUrl(thenExit=True):
  """The tutorial suggests requestb.in; and there, the problem does NOT appear!"""
  
  WEBHOOK="http://requestb.in/17v5yh31"
  print "pay here:"
  print cbCheckoutUrl(webhook="http://requestb.in/17v5yh31")
  print "then check the results on:\n%s?inspect" % WEBHOOK
  if thenExit: exit()  


def makePage(HTML):
  """html page with CSS"""
  return ('<html><head><base target="_blank"><link rel="stylesheet" '
          'href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">'
          '<style>body{padding:10px}</style></head><body>\n%s\n</body></html>' % HTML)
  

def html_clickForCheckout(url, last=None):
  """payment_url link for easy clicking. iframe for GET /hook/ results."""
  
  HTML= ('<h1>Webhook for Coinbase Notifications %s</h1>' % VERSION )
  
  HTML+=('<p>Please pay on ' 
         '<a href="%s">%s</a><br/>'
         'with sandbox money to trigger the callback from Coinbase, '
         'then reload the <a href="/hook">/hook</a> '
         'iframe below.</p>' )
  
  HTML+=('<p><button onclick="reload()">Reload</button> last notification:</p>'
         '<iframe id="001" src="/hook" width=1200 height=300>Try again '
         'in a browser which can do frames, sorry.</iframe><p>&nbsp;</p>'
         '<script>function reload(){'
         'document.getElementById("001").contentWindow.location.reload();}'
         '</script>')
  
  HTML+=('<p>Next:<ul><li>'
         '<a href="https://github.com/drandreaskrueger/coinbaseTestbed">'
         'sourcecode</a> of this</li><li>my Coinbase app '
         '<a href="http://208.68.38.174:8000/buyme">/buyme/</a></li></ul>')
  
  HTML+=('<hr/><pre>(C) 2016 Andreas Krueger\'s donation ware = If you like '
         'this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC</pre>')
    
  return makePage( HTML % (url, url) )


def headersTable(request):
  """all headers of the request, nicely table'd"""
  
  return "\n".join( ["%18s: %s" % (K, V) 
                     for K, V in request.headers.items()] )


def verify_callback(body, headers, dbg=False):
  """
  Verifies that the body is correctly signed, 
  with 'coinbase-callback.pub' public key
  See 'verify_callback()_False.md'
  """ 
  if dbg: print headers['Cb-Signature']
  if dbg: print body
  client = Client(API_KEY, API_SECRET, base_api_uri=API_BACKEND_URL)
  return client.verify_callback(body, headers['Cb-Signature'])


def tryJsonOrPlain(text):
  """Return json formatted, if possible. Otherwise just return."""
  try:
    return pprint.pformat( json.loads( text ), indent=1 )
  except:
    return text


class HeaderPrinter(object):
  """WebServer for '/' route"""
  
  @cherrypy.expose
  def index(self):
    """Generate a Coinbase checkout, and show it, clickable"""
    payment_url = cbCheckoutUrl(webhook=MY_URL+"/hook/")
    return html_clickForCheckout(payment_url)


class HeaderPrinterWebService(object):
  """Webservice with GET and POST."""
  
  exposed = True 
  lastNotification="" # supersimple temporary storage

  def GET(self):
    """Returns the last notification (from RAM), or 'None'"""
    cherrypy.response.headers['Content-Type'] = 'text/plain'
    return self.lastNotification or "None"

  def POST(self, length=8):
    """The webhook: Accepts any data, saves to simple string in RAM."""
    
    request=cherrypy.request
    
    R = headersTable(request)
    divider = "\n" +"-"*70 + "\n"
    R+= divider

    body=request.body.read()
    
    verified = verify_callback(body, request.headers)
    R+= "coinbase.wallet.client.verify_callback() = %s" % verified 
    R+= divider
     
    R+= tryJsonOrPlain(body)
    self.lastNotification=R
    
    return "Thanks."
    # curl -X POST -d {"test":42} -H "Content-Type: application/json" http://localhost/hook  
    # curl -X POST -d {"test":42} -H "Content-Type: application/json" http://208.68.38.174/hook

  
if __name__ == '__main__':
  
  # test_cbCheckoutUrl(thenExit=True)
 
  conf = {
      '/hook': {
          'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
      },
      'global':    { 'server.socket_host': '0.0.0.0',
                     'server.socket_port': 80,
                    }
  }
  service = HeaderPrinter()
  service.hook = HeaderPrinterWebService()
  cherrypy.quickstart(service, '/', conf)

