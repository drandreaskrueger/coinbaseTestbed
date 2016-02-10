# client.verify_callback
It is the little bugs that can cost you much time during developing ...

## Newsflash:
They "hope to have a fix for that soon". 

Until then ... perhaps do not use coinbase apps? Because their callbacks might not be verifiable. 

## Live presentation

I implemented the test into my supersimple cherrypy webhook server:

* see it live at: http://208.68.38.174
* [cbWebhookPrinter.py](../cb/cbWebhookPrinter.py) --> verify_callback(body, headers)

Bug 3 is not solved. But I had an idea ...

---
---
---

## Bug 1 [fixed]
(When I tried this,) the Python [library page](https://github.com/coinbase/coinbase-python#merchant-callbacks) said:

> Merchant Callbacks  
> Verify callback authenticity  

    client.verify_callback(request.body, request.META['X-Signature']) # true/false
    
BUT there is no 'X-Signature' in request.META

     <type 'exceptions.KeyError'> 'X-Signature'
     
     print request.META.keys()
     ['RUN_MAIN', 'SERVER_SOFTWARE', 'SCRIPT_NAME', 'REQUEST_METHOD', 'SERVER_PROTOCOL', 'HOME', 'LANG', 'SHELL', 'SERVER_PORT', 'HTTP_CB_VERSION', 'HTTP_HOST', 'HTTP_ACCEPT', 'wsgi.version', 'wsgi.run_once', 'SSH_TTY', 'wsgi.errors', 'wsgi.multiprocess', 'MAIL', 'SSH_CONNECTION', 'PATH_INFO', 'SSH_CLIENT', 'LOGNAME', 'USER', 'QUERY_STRING', 'PATH', 'TERM', 'HTTP_USER_AGENT', 'HTTP_CONNECTION', 'SERVER_NAME', 'REMOTE_ADDR', 'SHLVL', 'wsgi.url_scheme', 'HTTP_CB_SIGNATURE', 'CONTENT_LENGTH', 'wsgi.input', 'wsgi.multithread', 'TZ', '_', 'GATEWAY_INTERFACE', 'OLDPWD', 'PWD', 'DJANGO_SETTINGS_MODULE', 'CONTENT_TYPE', 'wsgi.file_wrapper', 'REMOTE_HOST', 'HTTP_ACCEPT_ENCODING']
     
instead there is a 'HTTP_CB_SIGNATURE' (684-letters long) - the new name.

[Fixed] The library page was improved now.
	 
## Bug 2

    verify=client.verify_callback(request.body, request.META['HTTP_CB_SIGNATURE'])

... results in:

    <type 'exceptions.IOError'> [Errno 2] 
    No such file or directory: 
    u'/usr/local/lib/python2.7/dist-packages/coinbase/wallet/coinbase-callback.pub'

The ``pip install coinbase`` seems to be lacking that file ``coinbase-callback.pub``.

	locate *.pub
	
	ls -R /usr/local/lib/python2.7/dist-packages/coinbase
	
	/usr/local/lib/python2.7/dist-packages/coinbase:
    __init__.py  __init__.pyc  wallet

    /usr/local/lib/python2.7/dist-packages/coinbase/wallet:
    auth.py   client.py   compat.py   error.py   __init__.py   model.py   util.py
    auth.pyc  client.pyc  compat.pyc  error.pyc  __init__.pyc  model.pyc  util.pyc
	
so I manually downloaded that key:

    cd /usr/local/lib/python2.7/dist-packages/coinbase/wallet/
    wget https://raw.githubusercontent.com/coinbase/coinbase-python/master/coinbase/wallet/coinbase-callback.pub
    
**News**: Confirmed. And: "We hope to have a fix for that soon." 
	
### Bug 3

Now I could finally evaluate an arriving notification, with [client.verify_callback](https://github.com/coinbase/coinbase-python/blob/c29183bba2104f6260ef7a1b9b4267e003a6137d/coinbase/wallet/client.py#L546-L553):

	print client.verify_callback(request.body, request.META['HTTP_CB_SIGNATURE'])

BUT I get a

    False
	
These are example inputs:

    request.body:  
    {"id":"ebd32071-1a1c-5967-9bb8-e029b827bb8e","type":"wallet:orders:paid","data":{"resource":{"id":"f157428b-8ad8-5d6b-a7b0-7304153e79b7","code":"TJYMUE02","type":"order","name":"test","description":null,"amount":{"amount":"0.00010100","currency":"BTC"},"receipt_url":"https://www.coinbase.com/orders/9f48d154e06e9434ae86825dd8d5028a/receipt","resource":"order","resource_path":"/v2/orders/f157428b-8ad8-5d6b-a7b0-7304153e79b7","status":"paid","bitcoin_amount":{"amount":"0.00010100","currency":"BTC"},"payout_amount":null,"bitcoin_address":"mjSU7wACi27LoXUj6TWERGZUorcsAEMbSk","refund_address":"mx7B2hjGuEPV8MkQYy2Up3bFiUcUGTBuYB","bitcoin_uri":"bitcoin:mjSU7wACi27LoXUj6TWERGZUorcsAEMbSk?amount=0.000101\u0026r=https://sandbox.coinbase.com/r/56a7cc50ade0d644b7000150","notifications_url":null,"paid_at":"2016-01-26T19:43:16Z","mispaid_at":null,"expires_at":"2016-01-26T19:58:12Z","metadata":{},"created_at":"2016-01-26T19:43:12Z","updated_at":"2016-01-26T19:43:16Z","customer_info":null,"transaction":{"id":"ae0acc03-f1cb-5b9a-bef0-b5106ba11500","resource":"transaction","resource_path":"/v2/accounts/d8cd3bdd-e9b6-5b89-ac2e-0b5db0fa7ee3/transactions/ae0acc03-f1cb-5b9a-bef0-b5106ba11500"},"mispayments":[],"refunds":[]}},"user":{"id":"8a7b0da0-ff92-5cb6-b42c-2b0d5c26e438","resource":"user","resource_path":"/v2/users/8a7b0da0-ff92-5cb6-b42c-2b0d5c26e438"},"account":{"id":"d8cd3bdd-e9b6-5b89-ac2e-0b5db0fa7ee3","resource":"account","resource_path":"/v2/accounts/d8cd3bdd-e9b6-5b89-ac2e-0b5db0fa7ee3"},"delivery_attempts":0,"created_at":"2016-01-26T19:43:17Z","resource":"notification","resource_path":"/v2/notifications/ebd32071-1a1c-5967-9bb8-e029b827bb8e"}
    
    CB_SIGNATURE:
      
    Ng+7+Pvye8oHadL07x9MZ8KNIDwajdrv1RkqiEPpHA93dlyc1OjB2Ruogevdq92G+X5grB1OAtuEgMTwh1tTs0UdN9dx0iLIV+Op84AJeE/5K471mDeyuscryLTgVLVlaryfTZtlcZI+DOXPwFvBe19TRcbJ6ZAHug6PwdAsXAqpvXKS18NdG8gh/Tti66IOUE6rKObgvcx2ZVOYXMIUcpJ/G7Hih33Qg4gIRyMk7+GIkX0EkTGNSJDL0z2U9h3GZ2G+iXniNzeI/cJK6hSpJe1NcRvAuA8qUXQ564BD7ZD31DTO3Kjy+rSASG20dJSh8QuxnfpYoDYshisX2PuHSR93fC9EcARre5HXd3yhr8L4S3c+IvySSpSOz6XZPIKtMLwkGnySln4aIx7hG5XJnpjRf3PEeWHwv19wXaqhRG/pXrnMEbU8aPqo9YDJ1AoLerOFtqzQCCp32MDenrxG8UAZuyusmiXW7n0qtaClzilBMtA6v+zQ77hYC4vbwmz+J2IeLGOq7BcQlMurCSSxRvh/lUDrZ9DBIxmHP7JFugMC+qXG/zOjTFA0zNbRL8zteI4iI8jnj5ITvG4wfhfP28m2Uy4FnMZUlnRDprrHtTHzY3dK7UkUo1UAtUR0wO2pbGzT890P4aYNCB0B7jOtv13UXy+ng8okkJxionxRO50=
    
    
Idea: Is that perhaps a sandbox specific problem?  
Does the sandbox use a different public key?


**News**: Yes. My hypothesis was confirmed. Different private key for sandbox, but undocumented.

---

## Donation ware!
(C) 2016 Andreas Krueger  
**If you like this, show it:** [BTC] [1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC](http://blockr.io/address/info/1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC)  
And: If you don't show that - then you show that you **don't** like this.