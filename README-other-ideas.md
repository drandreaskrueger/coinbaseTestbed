# ideas

More ideas, apart from those mentioned within the sourcecode.

## testing
https://developers.coinbase.com/docs/wallet/testing

### error list
When I read this sentence:

> Important: Different error types (id) can be added and removed over time so you should make sure your application accepts new ones as well.

I thought it makes sense to deliver the whole table (Error id, Code, Description) as an always up-to-date API function result, like:

https://api.coinbase.com/v2/error_codes

## Versioning

> All API calls should be made with a CB-VERSION header which guarantees that your call is using the correct API version. Version is passed in as a date (UTC) of the implementation in YYYY-MM-DD format.

https://developers.coinbase.com/api/v2#versioning

Can I choose ANY date (or does it have to be the release data of that version)? 
Where is the documentation for the version history?  
I tried a lot between 2011-01-01 and 2016-01-01, but so far haven't found differences. 

## HTTP verbs: OPTIONS

    import requests
    r = requests.options("https://api.sandbox.coinbase.com/v2/")
    print r.status_code
    
results in 
    404 
    
It would be good to:

> implement the OPTIONS method  
> http://docs.python-requests.org/en/latest/user/advanced/#http-verbs

## Notifications
When an API-key is created, and configured with a notifications callback URL, it would be useful to be able to simply trigger a dummy notification:

    from coinbase.wallet.client import Client
    client = Client(API_KEY, API_SECRET, base_api_uri=API_BACKEND_URL)
    notifications = client.trigger_dummy_callback()
	
to test my notification callback webhook.

