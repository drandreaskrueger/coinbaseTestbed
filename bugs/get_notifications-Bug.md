
# Bug: client.get_notifications()
The official code creates a  ``TypeError: unhashable type: 'dict'``  

And it is the little bugs that can cost you much time during developing ... 


### Details

https://api.sandbox.coinbase.com ... 'client.get_notifications()' is ill somehow!   

    TypeError: unhashable type: 'dict'

(with some accounts, e.g. ['0a30666a-33a5-5685-a81f-69be194d8602', '8a7b0da0-ff92-5cb6-b42c-2b0d5c26e438'])

    exception caught:  <type 'exceptions.TypeError'> unhashable type: 'dict'
    notifications = Client(API_KEY, API_SECRET, API_BACKEND_URL).get_notifications() [in BUG_get_notifications] line 41 of C:\Users\Andreas\Documents\GitHub-drandreaskrueger\github-drandreaskrueger-coinbaseTestbed\cb\cbNotificationsBug.py
    return self._make_api_object(response, Notification) [in get_notifications] line 264 of C:\Anaconda\lib\site-packages\coinbase\wallet\client.py
    obj.data = new_api_object(self, data, model_type) [in _make_api_object] line 161 of C:\Anaconda\lib\site-packages\coinbase\wallet\client.py
    return [new_api_object(client, v, cls) for v in obj] [in new_api_object] line 28 of C:\Anaconda\lib\site-packages\coinbase\wallet\model.py
    result[k] = new_api_object(client, v) [in new_api_object] line 25 of C:\Anaconda\lib\site-packages\coinbase\wallet\model.py
    cls = _resource_to_model.get(resource, None) [in new_api_object] line 15 of C:\Anaconda\lib\site-packages\coinbase\wallet\model.py

--> Coinbase.wallet.client.Client().get_notifications() is failing with a ''TypeError''.

Looks like you cannot properly handle your *own* dict-of-dicts? Complex beasts you have created there, so now you would need complexity-able programmers \*g\*.

### Examination

Trying to find out the reasons, by using my own auth-library ... This is the provoking data:

Authentication succeeded, user='0a30666a-33a5-5685-a81f-69be194d8602'  
Getting ALL notifications:
status_code : 200  
reason : OK  
url : https://api.sandbox.coinbase.com/v2/notifications  
encoding : utf-8  
text:

    {"pagination":{"ending_before":null,"starting_after":null,"limit":25,"order":"desc","previous_uri":null,"next_uri":null},"data":[{"id":"5984fb5f-faaf-53fe-a124-c27284a2d82e","type":"wallet:orders:mispaid","data":{"resource":{"id":"9d8fa4f2-0a64-5adc-b825-20217252b5dc","code":"KRIG1NJG","type":"order","name":"Time with a BitCoin Expert","description":"Buy time, and I skype with you.","amount":{"amount":"9.00","currency":"USD"},"receipt_url":"https://www.coinbase.com/orders/e0ff87fe61b77ff89f22a1b89c3909cf/receipt","resource":"order","resource_path":"/v2/orders/9d8fa4f2-0a64-5adc-b825-20217252b5dc","status":"expired","bitcoin_amount":{"amount":"0.00090000","currency":"BTC"},"payout_amount":null,"bitcoin_address":"n3bebTXAC2MAJsp6xx5Q9TudZtee27vyJ3","refund_address":null,"bitcoin_uri":"bitcoin:n3bebTXAC2MAJsp6xx5Q9TudZtee27vyJ3?amount=0.0009\u0026r=https://sandbox.coinbase.com/r/5699405cd59e1c01da000019","notifications_url":null,"paid_at":null,"mispaid_at":null,"expires_at":"2016-01-15T19:09:20Z","metadata":{"duration":"5 minutes","id":7},"created_at":"2016-01-15T18:54:20Z","updated_at":"2016-01-15T20:56:06Z","customer_info":null,"transaction":{"id":"616124b5-db6f-5038-99a5-196aec516ec8","resource":"transaction","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced/transactions/616124b5-db6f-5038-99a5-196aec516ec8"},"mispayments":[{"id":"3be30bea-2941-5e41-bb5f-9cd2d55d968a","amount":{"amount":"0.01650000","currency":"BTC"},"native_amount":{"amount":"165.00","currency":"USD"},"refund_address":"mjzKb2HrCxZ5DotKnZmGeCtdEESfhwtDNU","transaction":{"id":"616124b5-db6f-5038-99a5-196aec516ec8","resource":"transaction","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced/transactions/616124b5-db6f-5038-99a5-196aec516ec8"},"refund_transaction":null,"created_at":"2016-01-15T20:56:06Z","updated_at":"2016-01-15T20:56:06Z"}],"refunds":[]}},"user":{"id":"0a30666a-33a5-5685-a81f-69be194d8602","resource":"user","resource_path":"/v2/users/0a30666a-33a5-5685-a81f-69be194d8602"},"account":{"id":"f8dd37b1-8f12-5fbb-9889-d7599b398ced","resource":"account","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced"},"delivery_attempts":1,"created_at":"2016-01-15T20:56:06Z","resource":"notification","resource_path":"/v2/notifications/5984fb5f-faaf-53fe-a124-c27284a2d82e","delivered_at":"2016-01-15T20:56:07Z","delivery_response":{"message":"Notification delivered","body":"\u003chtml\u003e\u003cbody\u003eThanks.\u003c/body\u003e\u003c/html\u003e","status_code":200},"subscriber":{"type":"checkout","id":"3aeef4db-05ae-54a0-8954-562bf520aa11"}},{"id":"14aa1fe1-44cd-5c97-a39c-8407aed33a16","type":"wallet:orders:paid","data":{"resource":{"id":"0347e36d-8c1d-5266-963f-85d783edf8af","code":"8125NSY4","type":"order","name":"Time with a BitCoin Expert","description":"Buy time, and I skype with you.","amount":{"amount":"349.00","currency":"USD"},"receipt_url":"https://www.coinbase.com/orders/d137501a8ceee69482b8a2b7f1e8a668/receipt","resource":"order","resource_path":"/v2/orders/0347e36d-8c1d-5266-963f-85d783edf8af","status":"paid","bitcoin_amount":{"amount":"0.00090000","currency":"BTC"},"payout_amount":null,"bitcoin_address":"mi9HyjPoi4HLtBcKgGngToSUyZ549SJ1MR","refund_address":"muEtNYh9AmdUoVGz6seLHyZNVijKMTAox3","bitcoin_uri":"bitcoin:mi9HyjPoi4HLtBcKgGngToSUyZ549SJ1MR?amount=0.0009\u0026r=https://sandbox.coinbase.com/r/56993fe4124da0021e00000d","notifications_url":null,"paid_at":"2016-01-15T18:52:27Z","mispaid_at":null,"expires_at":"2016-01-15T19:07:21Z","metadata":{"duration":"1 day","id":6},"created_at":"2016-01-15T18:52:21Z","updated_at":"2016-01-15T18:52:27Z","customer_info":null,"transaction":{"id":"9b46b5a6-0216-5e0d-ac69-eced5a4af0db","resource":"transaction","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced/transactions/9b46b5a6-0216-5e0d-ac69-eced5a4af0db"},"mispayments":[],"refunds":[]}},"user":{"id":"0a30666a-33a5-5685-a81f-69be194d8602","resource":"user","resource_path":"/v2/users/0a30666a-33a5-5685-a81f-69be194d8602"},"account":{"id":"f8dd37b1-8f12-5fbb-9889-d7599b398ced","resource":"account","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced"},"delivery_attempts":1,"created_at":"2016-01-15T18:52:27Z","resource":"notification","resource_path":"/v2/notifications/14aa1fe1-44cd-5c97-a39c-8407aed33a16","delivered_at":"2016-01-15T18:52:28Z","delivery_response":{"message":"Notification delivered","body":"\u003chtml\u003e\u003cbody\u003eI got your message. Thanks.\u003c/body\u003e\u003c/html\u003e","status_code":200},"subscriber":{"type":"checkout","id":"a12e0497-6736-5cc9-bc9b-7663f091799d"}},{"id":"04e6b3c6-52c1-5a42-b3fb-cd09231bd9b5","type":"wallet:orders:paid","data":{"resource":{"id":"db7b805d-f3fe-5593-9b96-3aa7a6189e07","code":"8QX5R7N3","type":"order","name":"Time with a BitCoin Expert","description":"Buy time, and I skype with you.","amount":{"amount":"60.00","currency":"USD"},"receipt_url":"https://www.coinbase.com/orders/0a855c8bd0e5931b19e611fac10bdf67/receipt","resource":"order","resource_path":"/v2/orders/db7b805d-f3fe-5593-9b96-3aa7a6189e07","status":"paid","bitcoin_amount":{"amount":"0.00090000","currency":"BTC"},"payout_amount":null,"bitcoin_address":"mnAhiNJNjxn36zHPn4KoSKQW78yAzwR4P5","refund_address":"mxVGuA8yabRhEsLMFj1aE8r9Zv3pn3Kgbr","bitcoin_uri":"bitcoin:mnAhiNJNjxn36zHPn4KoSKQW78yAzwR4P5?amount=0.0009\u0026r=https://sandbox.coinbase.com/r/56993efb124da00209000012","notifications_url":null,"paid_at":"2016-01-15T18:48:36Z","mispaid_at":null,"expires_at":"2016-01-15T19:03:27Z","metadata":{"duration":"1 hour","id":5},"created_at":"2016-01-15T18:48:27Z","updated_at":"2016-01-15T18:48:36Z","customer_info":null,"transaction":{"id":"b69592a5-f14d-539b-b760-76b5a3df1903","resource":"transaction","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced/transactions/b69592a5-f14d-539b-b760-76b5a3df1903"},"mispayments":[],"refunds":[]}},"user":{"id":"0a30666a-33a5-5685-a81f-69be194d8602","resource":"user","resource_path":"/v2/users/0a30666a-33a5-5685-a81f-69be194d8602"},"account":{"id":"f8dd37b1-8f12-5fbb-9889-d7599b398ced","resource":"account","resource_path":"/v2/accounts/f8dd37b1-8f12-5fbb-9889-d7599b398ced"},"delivery_attempts":1,"created_at":"2016-01-15T18:48:36Z","resource":"notification","resource_path":"/v2/notifications/04e6b3c6-52c1-5a42-b3fb-cd09231bd9b5","delivered_at":"2016-01-15T18:48:37Z","delivery_response":{"message":"Notification delivered","body":"\u003chtml\u003e\u003cbody\u003eI got your message. Thanks.\u003c/body\u003e\u003c/html\u003e","status_code":200},"subscriber":{"type":"checkout","id":"c87c5f9d-3509-5746-88c0-f75c201a4b44"}}]}

That should help to debug your code.

---

### **News**

They'll  "be taking a look at it soon."

---

## Donation ware!
(C) 2016 Andreas Krueger  
**If you like this, show it:** [BTC] [1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC](http://blockr.io/address/info/1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC)  
And: If you don't show that - then you show that you **don't** like this.  
