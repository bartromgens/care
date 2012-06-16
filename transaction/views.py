from django.template import RequestContext
from django.shortcuts import render_to_response
from itertools import chain
from transaction.models import Transaction
from transactionreal.models import TransactionReal
from base.views import BaseView
from transaction.forms import NewTransactionForm
from userprofile.models import UserProfile

class BuyerDetailView(BaseView):

  template_name = "transaction/about.html"
  context_object_name = "transaction"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(BuyerDetailView, self).get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    transactions = Transaction.objects.filter(buyer__id=kwargs['buyerId'])
    context['transaction_list'] = transactions
    return context
    
class TransactionView(BaseView):
  template_name = "transaction/index.html"
  context_object_name = "transaction"
  
  def get_context_data(self, **kwargs):
    context = super(TransactionView, self).get_context_data(**kwargs)
    transactions = Transaction.objects.order_by('date')[:50].reverse()
    context['latest_transactions_list'] = transactions
    return context
    
    
class MyTransactionView(BaseView):
  template_name = "transaction/mytransactions.html"
  context_object_name = "my transactions"
  
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
    context = super(MyTransactionView, self).get_context_data(**kwargs)
    user = self.request.user
    buyerTransactions = self.getBuyerTransactions(user.id)
    consumerTransactions = self.getConsumerTransactions(user.id)
    full_list = list(chain(buyerTransactions, consumerTransactions))
    full_list_sorted = sorted(full_list, key=lambda instance: instance.date, reverse=True)
    
    context['buyer_transactions'] = self.getBuyerTransactions(user.id)
    context['consumer_transactions'] = self.getConsumerTransactions(user.id)
    context['full_list'] = full_list_sorted
    context['transactionssection'] = True
    return context# Create your views here.
    
class SelectGroupTransactionView(BaseView):
  template_name = "transaction/newselectgroup.html"
  context_object_name = "select transaction group"
  
  def get_context_data(self, **kwargs):    
    context = super(SelectGroupTransactionView, self).get_context_data(**kwargs)
    
    userProfile = UserProfile.objects.get(user=self.request.user)
    groupaccounts = userProfile.groupAccounts.all
    context['groupaccounts'] = groupaccounts
    context['transactionssection'] = True
    
    return context
    
def newTransaction(request, groupAccountId):
  def errorHandle(error):
    kwargs = {'user' : request.user,'groupAccountId' : groupAccountId}
    form = NewTransactionForm(**kwargs)
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      context['transactionssection'] = True
    return render_to_response('transaction/new.html', context)
          
  if request.method == 'POST': # If the form has been submitted...
    kwargs = {'user' : request.user,'groupAccountId' : groupAccountId}
    form = NewTransactionForm(request.POST, **kwargs) # A form bound to the POST data
    
    if form.is_valid(): # All validation rules pass
      form.save()
      context = RequestContext(request)

      if request.user.is_authenticated():
        context['user'] = request.user
        context['isLoggedin'] = True
        context['transactionssection'] = True

      return render_to_response('transaction/newsuccess.html', context)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  
  else:
    kwargs = {'user' : request.user,'groupAccountId' : groupAccountId}
    form = NewTransactionForm(**kwargs) # An unbound form
    context = RequestContext(request)
    context['form'] = form
    context['transactionssection'] = True
    
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
    return render_to_response('transaction/new.html', context)