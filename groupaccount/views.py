from base.views import BaseView
from groupaccount.forms import NewGroupAccountForm
from transaction.models import Transaction
from transaction.views import MyTransactionView
from userprofile.models import UserProfile

from django.contrib.auth.models import Group
from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)


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

  def getActiveMenu(self):
    return 'group'
  
  def getTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    return transactions
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(MyGroupAccountsView, self).get_context_data(**kwargs)
    user = self.request.user

    userProfile = UserProfile.objects.get(user=user)
    groupAccounts = userProfile.groupAccounts.all()
    
    accountView = MyTransactionView()
    
    for groupAccount in groupAccounts:
      groupBalance = 0.0
      groupAccount.userProfiles = UserProfile.objects.filter(groupAccounts=groupAccount)
      for userProfile in groupAccount.userProfiles:
        userProfile.balanceFloat = MyTransactionView.getBalance(accountView, groupAccount.id, userProfile.id)
        userProfile.balance = '%.2f' % userProfile.balanceFloat
        logger.debug(userProfile.balanceFloat)
        groupBalance += userProfile.balanceFloat
        logger.debug('groupBalance: ' + str(groupBalance))
      groupAccount.groupBalance = '%.2f' % groupBalance
      groupAccount.groupBalanceFloat = '%.3g' % groupBalance
      groupAccount.balanceVerified = bool(abs(groupBalance) < 1e-9)
      
    
    for groupAccount in groupAccounts:
      logger.warning(groupAccount.name) 
      for userProfile in groupAccount.userProfiles:
        logger.warning(userProfile.displayname + ' ' + userProfile.balance)  

    context['groups'] = groupAccounts
    context['groupssection'] = True
    return context# Create your views here.


class NewGroupAccountView(FormView, BaseView):
  template_name = 'groupaccount/new.html'
  form_class = NewGroupAccountForm
  success_url = '/groupaccount/new/success/'
  
  def getActiveMenu(self):
    return 'accounts'
   
  def getGroupAccountId(self):
    if 'groupAccountId' in self.kwargs:
      return self.kwargs['groupAccountId']
    else:
      logger.debug(self.request.user.id)
      user = UserProfile.objects.get(user=self.request.user)
      if user.groupAccounts.count():
        return user.groupAccounts.all()[0].id
      else:
        return 0
  
  def get_context_data(self, **kwargs):
    logger.debug('NewRealTransactionView::get_context_data() - groupAccountId: ' + str(self.getGroupAccountId()))
    context = super(NewGroupAccountView, self).get_context_data(**kwargs)
    
    form = NewGroupAccountForm()
    context['form'] = form
    
    return context
