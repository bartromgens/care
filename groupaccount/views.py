from itertools import chain
from django.contrib.auth.models import Group
#from accounts.models import Account
from transaction.models import Transaction
from transactionreal.models import TransactionReal
from base.views import BaseView
from userprofile.models import UserProfile

class GroupsView(BaseView):
  template_name = "groupaccount/index.html"
  context_object_name = "groups"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(GroupsView, self).get_context_data(**kwargs)
    groups = Group.objects.all()

    context['groups'] = groups
    context['groupssection'] = True
    return context# Create your views here.
    
    
class MyGroupAccountsView(BaseView):

  template_name = "groupaccount/myaccounts.html"
  context_object_name = "my groups"

  def getTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    return transactions
  
  def getNumberOfTransactions(self, buyerId):
    transactions = Transaction.objects.all()
    return len(transactions)
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(MyGroupAccountsView, self).get_context_data(**kwargs)
    user = self.request.user

    userProfile = UserProfile.objects.get(user=user)
#    self.logger.warning(userProfile)
    groupAccounts = userProfile.groupAccounts
    
    accountView = AccountDetailView()
    groupBalance = 0.0
    
    for groupAccount in groupAccounts:
#      self.logger.warning(groupAccount.name)
      groupAccount.userProfiles = UserProfile.objects.filter(groupAccounts=groupAccount)
      for userProfile in groupAccount.userProfiles:
        userProfile.balanceFloat = AccountDetailView.getBalance(accountView, groupAccount.id, userProfile.id)
        userProfile.balance = '%.2f' % userProfile.balanceFloat
        groupBalance += userProfile.balanceFloat
#        self.logger.warning(userProfile.balance)
      groupAccount.groupBalance = '%.2f' % groupBalance
      
    self.logger.warning(groupAccounts.all()) 
    
    for groupAccount in groupAccounts.all():
      for userProfile in groupAccount.userProfiles:
        self.logger.warning(groupAccount.userProfiles)  
    
    context['groups'] = groupAccounts
    context['groupssection'] = True
    return context# Create your views here.
        
class AccountDetailView(BaseView):
  template_name = "transaction/mytransactions.html"
  context_object_name = "account details"
  
  def getBuyerTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % (transaction.amount)
      transaction.amountPerPersonFloat = transaction.amount
    return transactions
    
  def getConsumerTransactions(self, consumerId):
    transactions = Transaction.objects.filter(consumers__id=consumerId)
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % (-1*transaction.amount/transaction.consumers.count())
      transaction.amountPerPersonFloat = (-1*transaction.amount/transaction.consumers.count())
    return transactions
    
  def getBalance(self, groupAccountId, userProfileId):
    buyerTransactions = Transaction.objects.filter(groupAccount__id=groupAccountId, buyer__id=userProfileId)
    consumerTransactions = Transaction.objects.filter(groupAccount__id=groupAccountId, consumers__id=userProfileId)

    senderRealTransactions = TransactionReal.objects.filter(groupAccount__id=groupAccountId, sender__id=userProfileId)
    receiverRealTransactions = TransactionReal.objects.filter(groupAccount__id=groupAccountId, receiver__id=userProfileId)
    
    totalBought = 0.0
    totalConsumed = 0.0
    
    totalSent = 0.0
    totalReceived = 0.0

    for transaction in buyerTransactions:
      totalBought += transaction.amount
      
    for transaction in consumerTransactions:
      nConsumers = transaction.consumers.count()
      totalConsumed += transaction.amount / nConsumers
      
    for transaction in senderRealTransactions:
      totalSent += transaction.amount
      
    for transaction in receiverRealTransactions:
      totalReceived += transaction.amount
      
    balance = (totalBought + totalSent - totalConsumed - totalReceived)
    
    return balance
  
  def getNumberOfBuyerTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    return len(transactions)
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(AccountDetailView, self).get_context_data(**kwargs)
    user = self.request.user
    buyerTransactions = self.getBuyerTransactions(user.id)
    consumerTransactions = self.getConsumerTransactions(user.id)
    full_list = list(chain(buyerTransactions, consumerTransactions))
    full_list_sorted = sorted(full_list, key=lambda instance: instance.date, reverse=True)
    
    context['buyer_transactions'] = self.getBuyerTransactions(user.id)
    context['consumer_transactions'] = self.getConsumerTransactions(user.id)
    context['full_list'] = full_list_sorted
    #context['balance'] = self.getBalance(accountId)
    return context# Create your views here.
