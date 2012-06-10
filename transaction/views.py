# some_app/views.py
#from django.views.generic import TemplateView, View
#from django.views.generic.edit import FormMixin
#from django.views.generic import DetailView
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.contrib.auth.models import User, Group

from transaction.models import Transaction
from base.views import BaseView
from transaction.forms import NewTransactionForm
from groupaccount.views import AccountDetailView
#from groupaccount.models import GroupAccount
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
    # Call the base implementation first to get a context
    context = super(TransactionView, self).get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    transactions = Transaction.objects.order_by('date')[:50].reverse()
    context['latest_transactions_list'] = transactions
    return context
    
class MyTransactionView(AccountDetailView):
  #template_name = "transactions/mytransactions.html"
  context_object_name = "my transactions"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
#    user = self.request.user
#    groups = user.groups.all()
    
    context = super(MyTransactionView, self).get_context_data(**kwargs)
    context['transactionssection'] = True
    #context['displayname'] = UserProfile.objects.get(user=self.request.user).displayname
    return context
    
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
    
def newTransaction(request, groupId):
  def errorHandle(error):
    kwargs = {'user' : request.user,'groupId' : groupId}
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
    kwargs = {'user' : request.user,'groupId' : groupId}
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
    kwargs = {'user' : request.user,'groupId' : groupId}
    form = NewTransactionForm(**kwargs) # An unbound form
    context = RequestContext(request)
    context['form'] = form
    context['transactionssection'] = True
    
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
    return render_to_response('transaction/new.html', context)