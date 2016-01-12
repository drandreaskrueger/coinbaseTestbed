'''
@title    cbPriceData.py
  
@purpose  play with price data from coinbase API    
  
@summary  Trying out the tutorial on   
          https://developers.coinbase.com/docs/wallet/guides/price-data
          --> Python 
          
          Found inconsistencies in tutorial. Run this to see.
          
  
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 11 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''

from cbWallet import cb

def showAsMoney(money):
  return "%s %s" % (money.currency, money.amount)

class cbPriceData(cb):
  
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
      
      

  def allCurrencies(self, debug=False):
    print "\nGenerating quite a cool table, please be patient. Getting the data ...\n1 Bitcoin = ..."
    counter, breakEveryX, storeEm = 0, 3, []
    
    # download prices for ALL currencies
    for curr in self.client.get_currencies().data:
      
      if debug and curr["id"]<"UUU": continue # for debugging: make faster by leaving out most
      
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
    
    if debug: print "(shortened table, due to debug=True)"
      
    print "\nopen '%s' to see same but with unicode characters" % filename
    


# tutorial inconsistent:
# https://developers.coinbase.com/docs/wallet/guides/price-data
# "As you can see above, Lawnmowers app displays"
# --> where is "above" ?     


# issue: in 'get_spot_price' Gold is supported, but unanswered!
# 0.00 XAU (Gold (Troy Ounce))

    
    
if __name__ == "__main__":
  C=cbPriceData()
  
  C.spotPrice()
  
  C.allCurrencies(debug=True)
  
