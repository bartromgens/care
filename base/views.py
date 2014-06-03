from groupaccount.models import GroupAccount
from userprofile.models import UserProfile
from transaction.models import Transaction
from transactionreal.models import TransactionReal
from groupaccountinvite.models import GroupAccountInvite 

from registration.backends.simple.views import RegistrationView
from django.views.generic import TemplateView

import logging
logger = logging.getLogger(__name__)


class BaseView(TemplateView):
  template_name = "base/base.html"
  context_object_name = "base"
  
  def getUserProfile(self):
    user = self.request.user
    return UserProfile.objects.get(user=user)
  
  def getActiveMenu(self):
    return ''
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(BaseView, self).get_context_data(**kwargs)
    if self.request.user.is_authenticated():
      userProfile = UserProfile.objects.get(user=self.request.user)
      invites = GroupAccountInvite.objects.filter(invitee=userProfile, isAccepted=False, isDeclined=False)
      context['user'] = self.request.user
      context['userprofile'] = userProfile
      context['hasInvites'] = invites.exists()
      context['nInvites'] = invites.count()
      context['displayname'] = userProfile.displayname
      context['activeMenu'] = self.getActiveMenu()
      context['isLoggedin'] = True
    return context


class NewRegistrationView(RegistrationView):
  
  def get_success_url(self, request, new_user):
    return '/'


class HomeView(BaseView):
  template_name = "base/index.html"
  context_object_name = "homepage"

  def getActiveMenu(self):
    return 'account'
  
  def getTransactions(self, buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId)
    return transactions
  
  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    userProfile = self.getUserProfile()
    
    groupAccounts = userProfile.groupAccounts.all()
    friends = UserProfile.objects.filter(groupAccounts__in=groupAccounts).distinct()
    
    transactionsAllSorted = Transaction.getTransactionsAllSortedByDate(userProfile.id) 
    transactionsRealAllSorted = TransactionReal.getTransactionsRealAllSortedByDate(userProfile.id)
        
    for groupAccount in groupAccounts:
      groupAccount = GroupAccount.addGroupAccountInfo(groupAccount, userProfile)
    
    myTotalBalanceFloat = 0.0
    for groupAccount in groupAccounts:
      myTotalBalanceFloat += groupAccount.myBalanceFloat
    
    myTotalBalance = '%.2f' % myTotalBalanceFloat
    context['myTotalBalance'] = myTotalBalance
    context['myTotalBalanceFloat'] = myTotalBalanceFloat
  
#     invitesAllSorted = GroupAccountInvite.getInvitesAllSortedByDate(userProfile)
    
    slowLastN = 5
#     context['invitesAll'] = invitesAllSorted[0:slowLastN]
    context['friends'] = friends
    context['transactionsAll'] = transactionsAllSorted[0:slowLastN]
    context['transactionsRealAll'] = transactionsRealAllSorted[0:slowLastN]
    context['groups'] = groupAccounts
    context['homesection'] = True
    return context
  
  
class AboutView(BaseView):
  template_name = "base/about.html"
  context_object_name = "about"
  
  def getActiveMenu(self):
    return 'about'
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(AboutView, self).get_context_data(**kwargs)
    context['aboutsection'] = True
    return context


class HelpView(BaseView):
  template_name = "base/help.html"
  context_object_name = "help"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(HelpView, self).get_context_data(**kwargs)
    context['helpsection'] = True
    return context
