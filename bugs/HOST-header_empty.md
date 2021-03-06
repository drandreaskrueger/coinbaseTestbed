# BUG [fixed]
## invalid HTTP_HOST header in callbacks to IP addresses
Man, they are difficult ...

--- 

## Newsflash: They've fixed it (February 10th)
Finally - they've done it. It needed 7 interactions, and almost 3 weeks. Hard to believe.  They kept on repeating: 

> *This has never been / is not an issue / anymore.* 

But then they've met me \*g\*:  If I had not *insisted* -fiercely- *three more times* after my initial submission - **this issue would probably have never been fixed**!

Not only a strange and difficult-to-find problem - but also a strange company.  And surprisingly penny-pinching: Over 100 mio USD of investors' hopes - but not willing to reward my good work, not even a bit? Is that wise? **Opulence degenerates**? 

But all that is *their* problem. My highest goal are simply well working systems. Read:

---


## Demo server (January 22st)

New 'foobar'-like demonstration code. Shows the problem in even less lines:

* [cbWebhookPrinter.py](../cb/cbWebhookPrinter.py) = Simple cherrypy webserver. 

LIVE: Running on my IP-only-droplet (at [digitalocean](https://github.com/drandreaskrueger/buyme/blob/master/_how-to/VPS.md)), so you can see the bug live:

* http://208.68.38.174/


Now the problem is isolated perfectly. Whew, all this had taken me many many hours to debug. Of course, at first I supposed that *my* code is buggy. What a strange problem.  

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

Finally, this is how I found the bug: After switching ON the Django logging (see [djangosite/loggingDebug.py](https://github.com/drandreaskrueger/buyme/blob/master/djangosite/loggingDebug.py) imported into [settings.py](https://github.com/drandreaskrueger/buyme/blob/master/djangosite/settings.py)) ...  

I was finally told, why it is not (200, OK) but (400, BAD REQUEST):

    Invalid HTTP_HOST header: ''. The domain name provided is not valid according to RFC 1034/1035.
    [19/Jan/2016 08:24:22] "POST /buyme/hook/9999999876543765456/ HTTP/1.1" 400 26
      
Perhaps your code tries to DNS-lookup the IP address of the ``notifications_url``, and when the result is "", it sets the HTTP_HOST header to ""?

    notifications_url='http://208.68.38.174:8000/buyme/hook/9999999876543765456/'
    
###Security implications
    
Until that was solved I had to run my server in ``DEBUG=False`` settings, of which the [django manual ](https://docs.djangoproject.com/en/1.9/ref/settings/#debug) says: "no no no!"

> A boolean that turns on/off debug mode.  
> Never deploy a site into production with DEBUG turned on.  
> Did you catch that? NEVER deploy a site into production with DEBUG turned on.


So a *security implication* did exist indeed: A 'domino effect security implication' = Your bug forced Django apps to run with highly insecure settings. See [chapter "Bug"](https://github.com/drandreaskrueger/buyme#bug) in README of my Coinbase example app /buyme/ . (That [/buyme/](https://github.com/drandreaskrueger/buyme) is actually the prototype app with which I originally found that bug in your system, very nice educational tool - you could consider buying it, actually.)

But I was told repeatedly: *No security implication*.  

I guess that is because only then they pay bug finding rewards? Perhaps they should reserve a 2nd budget to reward high-quality contributions like this one, which are not money-hacking, but still are improving the system. My 2 Satoshi.  
  

### The whole log:
See my app '[buyme](https://github.com/drandreaskrueger/buyme)' for details. But the following log tells you what you need to know:

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
    
Then, when a payment is authorized on that /checkout/ page, this arrives:

    Invalid HTTP_HOST header: ''. The domain name provided is not valid according to RFC 1034/1035.
    [19/Jan/2016 09:09:13] "POST /buyme/hook/9999999876543765456/ HTTP/1.1" 400 26
 
---

## Donation ware!
(C) 2016 Andreas Krueger  
**If you like this, show it:** [BTC] [1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC](http://blockr.io/address/info/1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC)  
*And if you do not show it - then ask yourself: Aren't you showing that you* **don't** *like this?*
