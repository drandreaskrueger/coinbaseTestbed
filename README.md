# coinbaseTestbed
Learning and improving the Coinbase tutorial https://developers.coinbase.com/

Please run these to see how coinbase works, and which inconsistencies & typos I have found in the official (Python) tutorial.

* [cbPersonal.py](cb/cbPersonal.py) = your API key goes here. Do all this with a [sandbox](https://sandbox.coinbase.com) account!
* [output](output/cbWallet.py.txt) of [cbWallet.py](cb/cbWallet.py) = testing: Guides ... [Create a wallet](https://developers.coinbase.com/docs/wallet/guides/bitcoin-wallet)
* [output](output/cbSendRequest.py.txt) of [cbSendRequest.py](cb/cbSendRequest.py) = testing: Guides ... [Send and Receive BTC](https://developers.coinbase.com/docs/wallet/guides/send-receive)
* [output](output/cbBuySellBtc.py.txt) of [cbBuySellBtc.py](cb/cbBuySellBtc.py) = testing: Guides ... [Buy and Sell BTC](https://developers.coinbase.com/docs/wallet/guides/buy-sell)
* [output](output/cbPriceData.py.txt) of [cbPriceData.py](cb/cbPriceData.py) = testing: Guides ... [Price Data](https://developers.coinbase.com/docs/wallet/guides/price-data)

The latter produces (among other things) a neat table of [all the currencies](output/1BitcoinInAllCurrencies-20160110.txt) (In non-fantasy exchange rates only when not on sandbox but on real api.).

The main purpose of my .py code is to try out all explained functions once, so that I  better understand the whole coinbase system. 

## inconsistencies, typos, bugs
The [tutorial](https://developers.coinbase.com) is not error-free. Throughout my .py code I have caught some exceptions caused by wrong syntax, or implementation. You see them either in the [source code](cb/) or in the [output](output/).

Additional to those, here are more:
* [client.get_notifications()](output/BUG_client.get_notifications()_with-API-answer.txt) has a real bug, some API answer is crashing the python library code.

Also see [my ideas](README-other-ideas.md) what else could be useful extensions.

---

All this is work in progress ... current version:

# v03


