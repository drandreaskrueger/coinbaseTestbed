# client.verify_callback

## Bug 1
The Python [library page](https://github.com/coinbase/coinbase-python#merchant-callbacks) says:

> Merchant Callbacks  
> Verify callback authenticity  

    client.verify_callback(request.body, request.META['X-Signature']) # true/false
    
BUT there is no 'X-Signature' in request.META

     <type 'exceptions.KeyError'> 'X-Signature'
     
     print request.META.keys()
     ['RUN_MAIN', 'SERVER_SOFTWARE', 'SCRIPT_NAME', 'REQUEST_METHOD', 'SERVER_PROTOCOL', 'HOME', 'LANG', 'SHELL', 'SERVER_PORT', 'HTTP_CB_VERSION', 'HTTP_HOST', 'HTTP_ACCEPT', 'wsgi.version', 'wsgi.run_once', 'SSH_TTY', 'wsgi.errors', 'wsgi.multiprocess', 'MAIL', 'SSH_CONNECTION', 'PATH_INFO', 'SSH_CLIENT', 'LOGNAME', 'USER', 'QUERY_STRING', 'PATH', 'TERM', 'HTTP_USER_AGENT', 'HTTP_CONNECTION', 'SERVER_NAME', 'REMOTE_ADDR', 'SHLVL', 'wsgi.url_scheme', 'HTTP_CB_SIGNATURE', 'CONTENT_LENGTH', 'wsgi.input', 'wsgi.multithread', 'TZ', '_', 'GATEWAY_INTERFACE', 'OLDPWD', 'PWD', 'DJANGO_SETTINGS_MODULE', 'CONTENT_TYPE', 'wsgi.file_wrapper', 'REMOTE_HOST', 'HTTP_ACCEPT_ENCODING']
     
instead there is a 'HTTP_CB_SIGNATURE' (684-letters long) - which is probably the new name???

Trying with that ...

	 
## Bug 2

    verify=client.verify_callback(request.body, request.META['HTTP_CB_SIGNATURE'])

... results in:

    <type 'exceptions.IOError'> [Errno 2] 
    No such file or directory: 
    u'/usr/local/lib/python2.7/dist-packages/coinbase/wallet/coinbase-callback.pub'

I guess the ``pip install coinbase`` is lacking that file ``coinbase-callback.pub``

	locate *.pub
	
	ls -R /usr/local/lib/python2.7/dist-packages/coinbase
	
	/usr/local/lib/python2.7/dist-packages/coinbase:
    __init__.py  __init__.pyc  wallet

    /usr/local/lib/python2.7/dist-packages/coinbase/wallet:
    auth.py   client.py   compat.py   error.py   __init__.py   model.py   util.py
    auth.pyc  client.pyc  compat.pyc  error.pyc  __init__.pyc  model.pyc  util.pyc
	
	
### Bug 3

Then I manually downloaded that key:

    cd /usr/local/lib/python2.7/dist-packages/coinbase/wallet/
    wget https://raw.githubusercontent.com/coinbase/coinbase-python/master/coinbase/wallet/coinbase-callback.pub
      
and now I could finally evaluate an arriving notification, with this command:

	verify=client.verify_callback(request.body, request.META['HTTP_CB_SIGNATURE'])
    print verify

BUT I get a

    False
	
These are the inputs:

    request.body:  
    {"id":"9e9bccb2-4945-5758-b3fd-9bf95a9b74ae","type":"wallet:orders:paid","data":{"resource":{"id":"6cd1265f-c1e7-53c4-86e0-a865fc7773bd","code":"T0Q2I24V","type":"order","name":"Buy Time with a Specialist in Cryptocurrencies.","description":"Let us SKYPE: I can CODE for you, RESEARCH your topics, ANALYZE your DATA, etc.","amount":{"amount":"200.00","currency":"USD"},"receipt_url":"https://www.coinbase.com/orders/cbadd77dd9282ce6641a9e251823d955/receipt","resource":"order","resource_path":"/v2/orders/6cd1265f-c1e7-53c4-86e0-a865fc7773bd","status":"paid","bitcoin_amount":{"amount":"0.00190000","currency":"BTC"},"payout_amount":null,"bitcoin_address":"n1J3gxZizHH8tvuNqNLwa47r8LG6M7WEGD","refund_address":"mscbFx7qRxfyTuJLLTLLw1uy3paosjw3Ts","bitcoin_uri":"bitcoin:n1J3gxZizHH8tvuNqNLwa47r8LG6M7WEGD?amount=0.0019\u0026r=https://sandbox.coinbase.com/r/569d304e124da0493b0001a2","notifications_url":null,"paid_at":"2016-01-18T18:35:00Z","mispaid_at":null,"expires_at":"2016-01-18T18:49:54Z","metadata":{"duration":"4 hours","price":"200 USD","id":8},"created_at":"2016-01-18T18:34:54Z","updated_at":"2016-01-18T18:35:00Z","customer_info":null,"transaction":{"id":"0c847fe5-6333-5c9c-89dc-35533f53f6b5","resource":"transaction","resource_path":"/v2/accounts/d8cd3bdd-e9b6-5b89-ac2e-0b5db0fa7ee3/transactions/0c847fe5-6333-5c9c-89dc-35533f53f6b5"},"mispayments":[],"refunds":[]}},"user":{"id":"8a7b0da0-ff92-5cb6-b42c-2b0d5c26e438","resource":"user","resource_path":"/v2/users/8a7b0da0-ff92-5cb6-b42c-2b0d5c26e438"},"account":{"id":"d8cd3bdd-e9b6-5b89-ac2e-0b5db0fa7ee3","resource":"account","resource_path":"/v2/accounts/d8cd3bdd-e9b6-5b89-ac2e-0b5db0fa7ee3"},"delivery_attempts":0,"created_at":"2016-01-18T18:35:00Z","resource":"notification","resource_path":"/v2/notifications/9e9bccb2-4945-5758-b3fd-9bf95a9b74ae"}
    
    request.META:  
    {'RUN_MAIN': 'true', 'SERVER_SOFTWARE': 'WSGIServer/0.1 Python/2.7.9', 'SCRIPT_NAME': u'', 'REQUEST_METHOD': 'POST', 'SERVER_PROTOCOL': 'HTTP/1.1', 'HOME': '/root', 'LANG': 'en_US.UTF-8', 'SHELL': '/bin/bash', 'SERVER_PORT': '8000', 'HTTP_CB_VERSION': 'BETA', 'HTTP_HOST': '', 'HTTP_ACCEPT': '*/*', 'wsgi.version': (1, 0), 'wsgi.run_once': False, 'SSH_TTY': '/dev/pts/5', 'wsgi.errors': <open file '<stderr>', mode 'w' at 0x7f47455e31e0>, 'wsgi.multiprocess': False, 'MAIL': '/var/mail/root', 'SSH_CONNECTION': '90.153.73.247 55787 208.68.38.174 22', 'PATH_INFO': u'/buyme/hook/9999999876543765456/', 'SSH_CLIENT': '90.153.73.247 55787 22', 'LOGNAME': 'root', 'USER': 'root', 'QUERY_STRING': '', 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'TERM': 'xterm', 'HTTP_USER_AGENT': 'Faraday v0.9.1', 'HTTP_CONNECTION': 'close', 'SERVER_NAME': 'debian-512mb-nyc1-01-BUYME', 'REMOTE_ADDR': '54.175.255.207', 'SHLVL': '1', 'wsgi.url_scheme': 'http', 'HTTP_CB_SIGNATURE': 'RzH8wD+axfL7oWFma23k0jH8Ua0aJWq/XdG9ZtwzUEp+H1340HCPYBoKRjAgHd3w2/WKznuZDIFSnMc3Vex4Uep8csB9la2UwJCsasgprFKv468vnMIu/Sjuwo0gmq4O0WHOWuhUIGfoyAijHTUc1o4s3zsmiM2xr26ytrh1bBVgh61KTwOVW4SkS3iqIO3STeupbF4C13ySwn8w2HxJezdbV66VXfbTwir07jBCKa6xqnNnhKZrTA1YFO6AMsR353zfd0L/J4exdiCOUZ2x8D3p2rzKXVZ6dddIKwJxcC7msDyBFS5bwR8EKiU5RVztmsZrKzg5swmsb+N4ozzOMYQMmuAOYTmq1JBvUmCVX29LvzoUSRMMJ0dBAs95b5k+LwnwwrXSX2C7XnqN208ZuKJk7BqU3IlONrdPIcDQ72hJcIyq+HuvFluxxLa8iBseXC3Yu0Ia5vwm2irpRFUwwyxmXcgsCYLs9tCoT5Sph2bVPmOH+t3h42eb34e4IB2KhAjuTqK5rxvvBg3JnxxbZpOUWFTAdZ5+vZUkwL/fE17+mCrEQ6cPkT3iY38kTcL9dSIeRfpt8Ki5DZMDgue7w5W+/V1TdpqzpVx8SrEJlbaRA9uXx3ZVHgILLUvMvPr0kp5ARnD9Wh+EvUTNI1BxFU7kqE0RK1e1XytpXxL17gk=', 'CONTENT_LENGTH': '1820', 'wsgi.input': <socket._fileobject object at 0x7f473b714cd0>, 'wsgi.multithread': True, 'TZ': 'UTC', '_': '/usr/bin/python', 'GATEWAY_INTERFACE': 'CGI/1.1', 'OLDPWD': '/root', 'PWD': '/root/buyme', 'DJANGO_SETTINGS_MODULE': 'djangosite.settings', 'CONTENT_TYPE': 'application/json', 'wsgi.file_wrapper': <class wsgiref.util.FileWrapper at 0x7f4741f394c8>, 'REMOTE_HOST': '', 'HTTP_ACCEPT_ENCODING': ''}



