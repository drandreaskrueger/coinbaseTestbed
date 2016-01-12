'''
@title    cbWallet.py

@purpose  Testing the coinbase Python API,
          and reporting errors in the tutorial

@summary: Learning the coinbase API, in depth.

          The following is partly from the tutorial pages.
          Plus own ideas, and improvements, and error reports.

          # tutorials:     https://developers.coinbase.com/
          # API reference: https://developers.coinbase.com/api/v2
          # found later:   https://github.com/coinbase/coinbase-python

          
@license:   (C) 2016 Andreas Krueger
@attention: If you like this, show it: [BTC] 1NvfRSDzXmwUdTjeqN8MAfmPCNHgwB8eiC  
@since      Created on 9 Jan 2016
@author:    Andreas Krueger  - github.com/drandreaskrueger

'''


# API authorization for coinbase. Import, or define here manually.
from cbPersonal import API_KEY, API_SECRET

# name of second account:
ACCOUNTNAME="piggybank" 

PRODUCTION = False
SANDBOX_URL = 'https://api.sandbox.coinbase.com'
PRODUCTION_URL=       'https://api.coinbase.com'
API_URL=PRODUCTION_URL if PRODUCTION else SANDBOX_URL 

# pip install coinbase # v2.0.3
from coinbase.wallet.client import Client


class cb (object):
  """
  coinbase - learning the tutorial on 
  https://developers.coinbase.com/docs/wallet/guides/bitcoin-wallet
  https://developers.coinbase.com/docs/wallet/guides/send-receive
  """
  
  def getClient(self):
    "establish connection"
    client = Client(API_KEY, API_SECRET, base_api_uri=API_URL)
    return client
  
  def __init__(self, client=None):
    "either start with given client, or open default one"
    if client==None: client = self.getClient()
    self.client = client

  def methods(self):
    print "\nall method names of coinbase.wallet.client.Client():"
    print "\n".join(dir(self.client))

  def showAccountsAndTransactions(self):
    print "\nget all accounts, for each show balance, and transactions:\n"
    accounts = self.client.get_accounts()
    for account in accounts.data:
      balance = account.balance
      print "%s: %s %s" % (account.name, balance.amount, balance.currency)
      print "number of transactions:", len(account.get_transactions().data)
      print "\n".join(["%s %s" % (t["type"],t["amount"]) for t in account.get_transactions().data])
      print
    
  def createAccount(self, name="New Account"):
    print "\ncreate account, and as access test ...show that it has an empty balance."
    
    account = self.client.create_account(name=name)
    balance = account.balance
    print "created: '%s' %s %s" % (account.name, balance.amount, balance.currency)
    return account


  def showAccountsDeleteEmptyOnes(self):
    "when the above resulted in excessively many new accounts, kill'em'all"
    print "\nDelete all accounts that are empty (no data):\n"
    accounts = self.client.get_accounts()
    for account in accounts.data:
      balance = account.balance
      print "%s: %s %s" % (account.name, balance.amount, balance.currency),
      
      if account.get_transactions().data==[] and account["type"]!="fiat":  
        #                  otherwise exception: Cannot delete a fiat account
        print "= found EMPTY account! (id=%s) Trying to delete now:" % account["id"]
        try:
          self.client.delete_account(account["id"])
        except Exception as e:
          print "exception caught: ", type(e), e
          print "Could NOT delete this account:\n", account, "\n"
        else:
          print "Done. Deleted.\n"
          
      else: print "= non-empty or fiat account (id=%s), continue." % account["id"]


  def findAccountIdsForName(self, name="New Account"):
    "returns all ids for all accounts with this name"
    ids=[]
    accounts = self.client.get_accounts()
    for account in accounts.data:
      if account["name"]==name:
        ids.append(account["id"])
    return ids
  
  def get_account(self,accId):
    "given id, return account"
    return self.client.get_account(accId)
  
  def firstAccountWithName(self,name):
    "given name, return first(?last?) account with that name"
    return self.get_account ( self.findAccountIdsForName(name)[0] )
  
      
  def sendMoneyTo(self, account, amount='0.001', description='For being awesome!'):
    print "\n(from primary account) send to (newly created address on) given account"
    
    # Get your primary account:
    primary_account = self.client.get_primary_account()
  
    # Generate a new bitcoin address
    address = account.create_address() # You created this account in the previous step
    print "newly created address: ", address.address
    
    # Send coins to the new account from your primary account:
    result = primary_account.send_money(to=address.address, amount=amount, currency='BTC', description=description)
    
    return result
    

  def get_primary_Account(self):
    "gets primary account, stores it for later, and returns it."
    self.PA = self.client.get_primary_account()
    return self.PA

  def recall_or_get_primary_Account(self):
    try:    primary_account=self.PA
    except: primary_account=self.PA=self.get_primary_Account()
    return primary_account

  def printLastTxOnPrimary(self):
    print "\nGet all transactions ... ",
    
    primary_account = self.recall_or_get_primary_Account()
    
    # tutorial improvement:
    # tutorial says to use [-1] to get the last transaction;
    # print "last tx:\n", primary_account.get_transactions()[-1]
    
    # but actually, I need to use [0] to get the last transaction.
    print "view the last tx:\n", primary_account.get_transactions()[0]
    
  def refreshAndShowPrimary(self):
    "After some time, the transaction should complete and your balance should update"
    PA=self.recall_or_get_primary_Account()
    print "\nRefresh ...", 
    PA.refresh()
    balance = PA.balance
    print "primary account '%s': %s %s" % (PA.name, balance.amount, balance.currency)
    
  def idsOfPendingTx(self, account):
    "of all tx of acc, return the ids of those with status pending"
    txs=account.get_transactions()
    return [(tx["id"],str(tx["amount"]),tx["type"]) 
            for tx in txs.data if tx["status"]=="pending"]
  
  def showPending(self):
    print "\npending transactions on all my accounts:"
    
    for account in self.client.get_accounts().data:
      print account["name"], self.idsOfPendingTx(account)
    
import random

def random2Digits():
  return int(random.random()*99 + 1)

def randomAdjective():
  nice=["awesome", "wonderful", "lovely", "great", "nice", "fantastic", "helpful"]
  return random.choice(nice)

def sendToSecondAccount(C, name=ACCOUNTNAME):
  print "\nSending to second account of mine:\n"  
  ids=C.findAccountIdsForName(name)
  
  if ids==[]:
    account=C.createAccount(name)
  else:
    print "Choose the first account which has that name '%s': " %name, 
    account=C.firstAccountWithName(name)
    print account["id"]
    
  print account["name"], str(account["balance"]), "(%s to %s)" % (account ["created_at"], account["updated_at"]) 
  

  amount = '0.00%s' % random2Digits()
  description = 'for being %s!' % randomAdjective()

  result=C.sendMoneyTo(account, amount, description )
  print "Sending - done. Result: %s\n%s" % (type(result), result)

def listOfTransactions(C):
  print "\nFinding out what kind of beast a list of transactions actually is:"
  
  print "get all transactions from primary account ..."
  txs=C.get_primary_Account().get_transactions()
  
  print "Done. Trying to iterate:"
  try:
    print [tx["id"] for tx in txs]
  except Exception as e:
    print "exception caught: ", type(e), e
  
  print "inconsistent?"
  print [type(tx) for tx in txs], " versus ",
  print type( txs[0] ), "and", type( txs[1] ) 
  
  print "\nThis does work:"
  print [tx["id"] for tx in txs["data"]]
  
  print "This does work too:"
  print [tx["id"] for tx in txs.data]

def pause():
  raw_input("\nPress Enter to continue...")
  
def showAllTransactionsDetailsWithPause(account):
  print "Show ALL transactions of account %s:\n" % account["id"]
  for tx in account.get_transactions().data:
    print tx["amount"], tx["description"], tx["id"]
    print tx
    pause()
  
def tryWalletFunctions():
  C=cb()
  
  print C
  C.methods()

  C.showAccountsAndTransactions()
  pause()
  
  account=C.createAccount(name="lalala")
  print account
  pause()
  
  C.showAccountsDeleteEmptyOnes()
  pause()
  
  sendToSecondAccount(C)
  pause()
  
  
  C.printLastTxOnPrimary()
  pause()
  
  C.refreshAndShowPrimary()  
    
  listOfTransactions(C)
  pause()
  
  C.showPending()
  
  showAllTransactionsDetailsWithPause( C.get_primary_Account() )
 

if __name__ == "__main__":

  tryWalletFunctions()
  

