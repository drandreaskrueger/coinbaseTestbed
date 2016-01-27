# coinbaseTestbed
Learning (and improving) the Coinbase tutorial https://developers.coinbase.com/

## Inconsistencies, typos, bugs
I could find these bugs in the Python library, and/or the server code:   

* [client.get_notifications()](output/cbNotificationsBug.py.txt) - the [official code](cb/cbNotificationsBug.py) creates a ``TypeError: unhashable type: 'dict'``.
* [verify_callback()](bugs/verify_callback()_False.md) - missing data, and a bug?
* [invalid (empty) HOST header](bugs/HOST-header_empty.md) - Django refuses your POST requests (RFC 1034/1035).
* "[*Do you want to add it?*](bugs/Do-you-want-to-add-it_But-no-way-to-say-YES.png)" (a fee) when small amounts - but no way to answer. Clicking "Pay" doesn't work.



*Additional to those*:

* Please read [my ideas](README-other-ideas.md) what else could be useful extensions, for future versions of your API.
* In my .py code below ... I have *caught some exceptions* caused by wrong syntax, or implementation, while I was working through your [tutorial](https://developers.coinbase.com). You'll see them either in the [source code](cb/) or in the [output](output/).

## Working code
The main purpose of my .py code was to try out all explained functions once, so that I  better understand the whole coinbase system. But I am publishing it, because it might help others.

Intended for:
* Coinbase newbies: Run these one by one, to see how coinbase works. 
* Coinbase devs: And which inconsistencies & typos I have found in the official (Python) tutorial.

Chapter by chapter:
* [output](output/cbWallet.py.txt) of [cbWallet.py](cb/cbWallet.py) = testing: Guides ... [Create a wallet](https://developers.coinbase.com/docs/wallet/guides/bitcoin-wallet)
* [output](output/cbSendRequest.py.txt) of [cbSendRequest.py](cb/cbSendRequest.py) = testing: Guides ... [Send and Receive BTC](https://developers.coinbase.com/docs/wallet/guides/send-receive)
* [output](output/cbBuySellBtc.py.txt) of [cbBuySellBtc.py](cb/cbBuySellBtc.py) = testing: Guides ... [Buy and Sell BTC](https://developers.coinbase.com/docs/wallet/guides/buy-sell)
* [output](output/cbPriceData.py.txt) of [cbPriceData.py](cb/cbPriceData.py) = testing: Guides ... [Price Data](https://developers.coinbase.com/docs/wallet/guides/price-data) (*) 
* [output](output/cbAuthenticationBasics.py.txt) of [cbAuthenticationBasics.py](cb/cbAuthenticationBasics.py) - Custom authentication for Coinbase API = Guides ... [API Key Authentication](https://developers.coinbase.com/docs/wallet/api-key-authentication#making-a-request)
* [output](output/cbNotificationsBug.py.txt) of [cbNotificationsBug.py](cb/cbNotificationsBug.py) - uses that custom authentication to get the provoking data. I hope that helps you to debug it.


Do all this with a [sandbox](https://sandbox.coinbase.com) account!
* [cbPersonal.py](cb/cbPersonal.py) = your API key goes here. 

(*) This produces (among other things) a neat table of [all the currencies](output/1BitcoinInAllCurrencies-20160110.txt) (In non-fantasy exchange rates only when not on sandbox but on real api.).

All this is work in progress, perhaps more to come ... current version: **v07**

---


## donation ware!
(C) 2016 Andreas Krueger  
**If you like this, show it:** [BTC] [1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC](http://blockr.io/address/info/1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC)   
No Coinbase account yet? Please [use my referral](https://www.coinbase.com/join/andreaskrueger), to give me and you 10$ bonus.  
