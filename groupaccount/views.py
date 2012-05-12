from django.views.generic import TemplateView
from django.views.generic import DetailView
from itertools import chain
from django.contrib.auth.models import User, Group
#from accounts.models import Account
from transaction.models import Transaction
from base.views import BaseView

class GroupsView(BaseView):
  template_name = "accounts/index.html"
  context_object_name = "groups"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(GroupsView, self).get_context_data(**kwargs)
    groups = Group.objects.all()
    accountView = AccountDetailView()

    context['groups'] = groups
    context['groupssection'] = True
    return context# Create your views here.
    
    
class MyGroupsView(BaseView):
  template_name = "accounts/myaccounts.html"
  context_object_name = "my groups"
  
  def getTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    return transactions
  
  def getNumberOfTransactions(self, buyerId):
    transactions = Transaction.objects.all()
    return len(transactions)
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(MyGroupsView, self).get_context_data(**kwargs)
    user = self.request.user
    groups = Group.objects.filter(user=user)
    
    accountView = AccountDetailView()
    groupBalance = 0.0
    
    for group in groups:
      group.users = group.user_set.all()
      for user in group.users:
	user.balanceFloat = AccountDetailView.getBalance(accountView, group.id, user.id)
	user.balance = '%.2f' % user.balanceFloat
	groupBalance += user.balanceFloat
      group.groupBalance = '%.2f' % groupBalance
      
    context['groups'] = groups
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
    
  def getBalance(self, groupId, userId):
    buyerTransactions = Transaction.objects.filter(group__id=groupId, buyer__id=userId)
    consumerTransactions = Transaction.objects.filter(group__id=groupId, consumers__id=userId)
    
    totalBought = 0.0
    totalConsumed = 0.0

    for transaction in buyerTransactions:
      totalBought += transaction.amount
	
    for transaction in consumerTransactions:
      nConsumers = transaction.consumers.count()
      totalConsumed += transaction.amount / nConsumers
      
    balance = (totalBought - totalConsumed)
    
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
