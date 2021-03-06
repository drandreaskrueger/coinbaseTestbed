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
      try:
        sell = account.sell(amount='0.001',
                        currency="BTC",
                        payment_method=payment_method.id)
        print "Sold!\n", sell
      except Exception as e:
        print "exception caught: ", type(e), e
      
    if float(buy_price.amount) <= buy_price_threshold:
      print "Decide to buy ... ",
      try:
        buy = account.buy(amount='0.001',
                      currency="BTC",
                      payment_method=payment_method.id)
        print "bought!\n", buy
      except Exception as e:
        print "exception caught: ", type(e), e
    

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
 
  
  
