'''
@title    cbBuySellBtc.py
  
@purpose  buy and sell bitcoin 
  
@summary  Trying out the tutorial on   
          https://developers.coinbase.com/docs/wallet/guides/buy-sell
          --> Python 
          
          Found inconsistencies, and typos in tutorial. Run this to see.
          
  
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 10 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''

from cbWallet import cb, pause

def showAsMoney(money):
  return "%s %s" % (money.currency, money.amount)

class cbBuySellBtc(cb):
  
  def get_payment_methods(self):
    return self.client.get_payment_methods()
  
  def tableLayout(self, PM):
    print "\nShowing payment methods: number=",
    pm=PM.data
    print len(pm)
    print 
    for k in pm[0].keys():
      if not k=="limits": 
        print "%20s: %40s %40s" % (k, pm[0][k], pm[1][k])
        
    print "\n%20s:" % "Limits"
    for i in (0,1):
      print "\n####### payment_method: %s #######" % pm[i]["name"]
      for category in pm[i]["limits"].keys():
        print "'%s' limits (%s):" % (category, pm[i]["name"]) 
        for L in pm[i]["limits"][category]:
          print L
      print 

  def amountWithCurrency(self, ):
    pass

  def inconsistency_PricesAreNotMoney(self):
    
    print "\nInconsistency in 'get_buy_price': Returns .APIObject not .Money"
    
    print "\nget the current buy price,  type=", 
    buy_price  = self.client.get_buy_price(currency='USD')
    print type(buy_price)
    
    print "amount of last transaction, type=", 
    amount=self.get_primary_Account().get_transactions()[0]["amount"]
    print type(amount)
    
    print "\nThe consequence: More difficult to cast to string:"
    print "easy: ", str(amount)
    print "*meh* ", str(buy_price)

  def buyAndSellBtc(self, buy_price_threshold  = 200, sell_price_threshold = 500):
    print"\nBuy OR Sell BTC for USD, depending on current price\n"
    
    buy_price  = self.client.get_buy_price(currency='USD')
    sell_price = self.client.get_sell_price(currency='USD')
    
    print "Buy Price : %s Threshold: %s" % (showAsMoney(buy_price), buy_price_threshold)
    print "Sell Price: %s Threshold: %s" % (showAsMoney(sell_price), sell_price_threshold)

    account = self.client.get_primary_account()
    payment_method = self.get_payment_methods()[0]
    
    ########## corrected in the following:
    ########## tutorial error 1: ruby syntax
    ########## tutorial error 2: >= not <=
    
    if float(sell_price.amount) >= sell_price_threshold:
      print "Decide to sell ...",
      sell = account.sell(amount='0.001',
                      currency="BTC",
                      payment_method=payment_method.id)
      print "Sold!\n", sell
      
    if float(buy_price.amount) <= buy_price_threshold:
      print "Decide to buy ... ",
      buy = account.buy(amount='0.001',
                    currency="BTC",
                    payment_method=payment_method.id)
      print "bought!\n", buy
      
      
  def spotPrice(self):
    print "\nGet spot price of BTC in given currency."
    currency_code="USD"
    try:
      print "\nwrong syntax in tutorial:  client.get_spot_price({currency: currency_code})"  
      price = self.client.get_spot_price({currency: currency_code})
    except Exception as e: print "exception caught: ", type(e), e
    
    print "\ncorrect syntax:\nclient.get_spot_price(currency=currency_code)\n"
    for currency_code in ['USD', 'EUR', 'CAD', 'YEN', 'XAU']:  # can also use EUR, CAD, etc.
      # Make the request
      price = self.client.get_spot_price(currency=currency_code)
      print 'Current bitcoin price in %s: %s %s' % (currency_code, price.amount, price.currency)
      
      

  def allCurrencies(self):
    print "\nGenerating quite a cool table, please be patient. Getting the data ...\n1 Bitcoin = ..."
    counter, breakEveryX, storeEm = 0, 3, []
    
    # download prices for ALL currencies
    for curr in self.client.get_currencies().data:
      
      # if curr["id"]<"UUU": continue # for debugging: make faster by leaving out most
      
      price = self.client.get_spot_price(currency=curr["id"])
      # name = repr(curr["name"])
      # name = unicode(curr["name"], errors='ignore')
      name = curr["name"].encode('utf-8')
      
      print '... in %s (%s): %s %s !' % (curr["id"], repr(name), price.amount, price.currency),
      counter+=1 
      if counter%breakEveryX==0: print
      
      # keep for later:
      storeEm.append({"price": float(price.amount), "curr":price.currency, "name": name})
  
    
    print "\nSort by price ...",
    storeEm.sort(key=lambda x:x["price"], reverse=True)
    yiehah=["{price:13.2f} {curr:s} ({name:s})\n".format(**p) for p in storeEm]
            
    print "done. Writing to file (because of unicode characters) ...", 
    filename="currencies2btc.txt"
    o=file(filename,"w")
    o.writelines(yiehah)
    o.close()
    
    print "done.\n\nHave you ever seen the world currencies in this cool order?\n"
    with file("currencies2btc.txt","r") as f:
      L=f.readlines()
    print "".join(L)
      
    print "\nopen '%s' to see same but with unicode characters" % filename
    

"""

# inconsistency in sandbox setup: 
# two different buy limits for payment method 'Test Bank *****7934'
# but both are "period_in_days": 1
# see this extract from    'C.tableLayout(C.get_payment_methods())'

'buy' limits (Test Bank *****7934):
{
  "period_in_days": 1, 
  "remaining": {
    "amount": "10000.00", 
    "currency": "USD"
  }, 
  "total": {
    "amount": "10000.00", 
    "currency": "USD"
  }
}
{
  "period_in_days": 1, 
  "remaining": {
    "amount": "25.00", 
    "currency": "USD"
  }, 
  "total": {
    "amount": "100.00", 
    "currency": "USD"
  }
}


"""

   
if __name__ == "__main__":
  C=cbBuySellBtc()
  
  C.tableLayout(C.get_payment_methods())
  pause()
  
  C.inconsistency_PricesAreNotMoney()
  pause()
  
  C.buyAndSellBtc()
  pause()
  print "\nNow again, with different thresholds:"
  C.buyAndSellBtc(20000,50000)
 
  
  
