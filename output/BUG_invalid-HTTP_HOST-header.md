# BUG: invalid HTTP_HOST header in callbacks to IP addresses
Whew, this took me many many hours to debug. What a strange problem.

### Symptom
when Coinbase sends a notification callback, my django server (if in production-mode) immediately refuses it with a (400, BAD REQUEST):

    [19/Jan/2016 08:24:22] "POST /buyme/hook/9999999876543765456/ HTTP/1.1" 400 26

(i.e. not one line of my own code is even called. That made it difficult to find the reason.) 

In contrast, when I do a manual curl on the same webhook:

    curl -X POST -d '{"reason":"testing"}' -H "Content-Type: application/json" http://208.68.38.174:8000/buyme/hook/9999999876543765456/

my django server is happily accepting it, and my own code gets executed, and a (200, OK) is returned. 

    Received POST request on 'hook/name' : 9999999876543765456 
    '90.153.73.247' is NOT a coinbase IP! trustIP=False
    [19/Jan/2016 08:44:18] "POST /buyme/hook/9999999876543765456/ HTTP/1.1" 200 33
    
### Finally found the reason:  RFC 1034/1035 

The bug was so difficult to find because:
* In Django it only happens when ``DEBUG=False`` ([*](https://docs.djangoproject.com/en/1.9/ref/settings/#debug)), i.e. when I wanted to go production, suddenly my server stopped accepting all your POST requests.   
* The problem is not visible in http://requestb.in callbacks. There it shows a proper "Host: requestb.in".
* (Perhaps it happens because my server is an IP-address-only server?)

Finally, this is how I found the bug: After switching ON the Django logging (see [djangosite/loggingDebug.py](../djangosite/loggingDebug.py) imported into [settings.py](../djangosite/settings.py)) ...  

I was finally told, why it is not (200, OK) but (400, BAD REQUEST):

    Invalid HTTP_HOST header: ''. The domain name provided is not valid according to RFC 1034/1035.
    [19/Jan/2016 08:24:22] "POST /buyme/hook/9999999876543765456/ HTTP/1.1" 400 26
      
Perhaps your code tries to DNS-lookup the IP address of the ``notifications_url``, and when the result is "", it sets the HTTP_HOST header to ""?

    notifications_url='http://208.68.38.174:8000/buyme/hook/9999999876543765456/'
    
Until that is solved I will have to run my server in ``DEBUG=False`` settings, of which the [django manual ](https://docs.djangoproject.com/en/1.9/ref/settings/#debug) says: "no no no!"

> A boolean that turns on/off debug mode.  
> Never deploy a site into production with DEBUG turned on.  
> Did you catch that? NEVER deploy a site into production with DEBUG turned on.

:-)  

So please contact me when you have solved this. Thanks!
  

### The whole log:
See my app '[buyme](https://github.com/drandreaskrueger/buyme)' for details.  

    Django version 1.9.1, using settings 'djangosite.settings'
    Starting development server at http://0.0.0.0:8000/

    showing webpage with form to input credentials
    [19/Jan/2016 09:08:43] "GET /buyme/ HTTP/1.1" 200 4027

    POST request received.
    Valid. Taking form entries, and creating a coinbase checkout.
    Using notifications_url='http://208.68.38.174:8000/buyme/hook/9999999876543765456/' for callback.
    checkout.warnings=None
    
    redirecting to coinbase: https://sandbox.coinbase.com/checkouts/900a2ae7be0c03d8d5ef702aa4209fdb
    [19/Jan/2016 09:09:02] "POST /buyme/ HTTP/1.1" 302 0
    
    Invalid HTTP_HOST header: ''. The domain name provided is not valid according to RFC 1034/1035.
    [19/Jan/2016 09:09:13] "POST /buyme/hook/9999999876543765456/ HTTP/1.1" 400 26
 
 
 