# ideas

More ideas, apart from those mentioned within the sourcecode.

## testing - error list
When I read this sentence in [/docs/wallet/testing](https://developers.coinbase.com/docs/wallet/testing):

> Important: Different error types (id) can be added and removed over time so you should make sure your application accepts new ones as well.

I thought this new function could make sense:

* https://api.coinbase.com/v2/error_codes

which would deliver the whole table (Error id, Code, Description) as an always up-to-date API function result.

## Versioning

> All API calls should be made with a CB-VERSION header which guarantees that your call is using the correct API version. Version is passed in as a date (UTC) of the implementation in YYYY-MM-DD format.

https://developers.coinbase.com/api/v2#versioning

Can I choose ANY date (or does it have to be the exact release data of that version)?   
Where is the documentation for the version history?  


## HTTP verbs: OPTIONS

    import requests
    r = requests.options("https://api.sandbox.coinbase.com/v2/")
    print r.status_code
    
results in 
    404 
    
It would be good to:

> implement the OPTIONS method  
> http://docs.python-requests.org/en/latest/user/advanced/#http-verbs

## Trigger notification callbacks
It would be useful to be able to simply trigger a dummy notification (after a new API-key is created, and configured with a notifications callback URL): 

    from coinbase.wallet.client import Client
    client = Client(API_KEY, API_SECRET, base_api_uri=API_BACKEND_URL)
    client.trigger_dummy_callback()
    
to test my notification callback webhook that accepts the POST requests.  

You will not believe how many *payments* I have done by now, just to debug my webhook-callback functionality (to find your [nasty bug](bugs/HOST-header_empty.md) alone costed me many dozens). A dummy callback would help a lot.

Similarly, for a specific checkout, with its own ``notifications_url`` 

    parameters={ "amount": amount, "currency": currency, 
                 "notifications_url" : "http://requestb.in/w2vw66w2" }
    checkout = client.create_checkout(**parameters)
    client.trigger_dummy_callback(id=checkout["id"])

Only useful during coding a new app, but it would have saved me a lot of time, actually.  

Thanks a lot, for considering this.