from base.views import BaseView
from groupaccount.forms import NewGroupAccountForm
from groupaccount.models import GroupAccount
from transaction.models import Transaction
from userprofile.models import UserProfile

from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)
   
    
class MyGroupAccountsView(BaseView):
  template_name = "groupaccount/myaccounts.html"
  context_object_name = "my groups"

  def getActiveMenu(self):
    return 'group'
  
  def getTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    return transactions
  
  def get_context_data(self, **kwargs):
    user = self.request.user
    userProfile = UserProfile.objects.get(user=user)
    userProfile.setShowTable(self.kwargs['tableView'])   
    groupAccounts = userProfile.groupAccounts.all()
    
    for groupAccount in groupAccounts:
      groupAccount = GroupAccount.addGroupAccountInfo(groupAccount, userProfile)

    context = super(MyGroupAccountsView, self).get_context_data(**kwargs)
    context['groups'] = groupAccounts
    context['groupssection'] = True
    return context# Create your views here.


class NewGroupAccountView(FormView, BaseView):
  template_name = 'groupaccount/new.html'
  form_class = NewGroupAccountForm
  success_url = '/account/new/success/'
  
  def get_form(self, form_class):
    return NewGroupAccountForm(**self.get_form_kwargs())   
  
  def getActiveMenu(self):
    return 'group'

  def form_valid(self, form):
    super(NewGroupAccountView, self).form_valid(form)
    groupAccount = form.save()
    userProfile = UserProfile.objects.get(user=self.request.user)
    userProfile.groupAccounts.add(groupAccount)
    userProfile.save()
    
    return HttpResponseRedirect('/group/new/success/')
  
  def get_context_data(self, **kwargs):
    context = super(NewGroupAccountView, self).get_context_data(**kwargs)
    
    form = NewGroupAccountForm(**self.get_form_kwargs())
    context['form'] = form
    return context


class SucessNewGroupAccountView(BaseView):
  template_name = 'groupaccount/newsuccess.html'
  
  def getActiveMenu(self):
    return 'accounts'
