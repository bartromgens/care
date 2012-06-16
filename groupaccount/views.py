from django.contrib.auth.models import Group
#from accounts.models import Account
from transaction.models import Transaction
from transaction.views import MyTransactionView
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
    groupAccounts = userProfile.groupAccounts.all()
    
    accountView = MyTransactionView()
    groupBalance = 0.0
    
    for groupAccount in groupAccounts:
      groupAccount.userProfiles = UserProfile.objects.filter(groupAccounts=groupAccount)
      for userProfile in groupAccount.userProfiles:
        userProfile.balanceFloat = MyTransactionView.getBalance(accountView, groupAccount.id, userProfile.id)
        userProfile.balance = '%.2f' % userProfile.balanceFloat
        groupBalance += userProfile.balanceFloat
      groupAccount.groupBalance = '%.2f' % groupBalance
      
    
    for groupAccount in groupAccounts:
      self.logger.warning(groupAccount.name) 
      for userProfile in groupAccount.userProfiles:
        self.logger.warning(userProfile.displayname + ' ' + userProfile.balance)  

    context['groups'] = groupAccounts
    context['groupssection'] = True
    return context# Create your views here.
