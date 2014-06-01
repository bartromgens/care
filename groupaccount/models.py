from django.db import models

#users = User.objects.filter(groups__name='monkeys')

class GroupAccount(models.Model):
  name = models.CharField(max_length=200)
  number = models.IntegerField(unique=True)
  #settings = models.ForeignKey(GroupSettings)
  
  def __str__(self):
    return self.name
  
  @staticmethod
  def addGroupAccountInfo(groupAccount, myUserProfile):
    from userprofile.models import UserProfile
    
    groupBalance = 0.0
    groupAccount.userProfiles = UserProfile.objects.filter(groupAccounts=groupAccount)
    for userProfile in groupAccount.userProfiles:
      userProfile.balanceFloat = UserProfile.getBalance(groupAccount.id, userProfile.id)
      userProfile.balance = '%.2f' % userProfile.balanceFloat
      groupBalance += userProfile.balanceFloat
    groupAccount.groupBalance = '%.2f' % groupBalance
    groupAccount.groupBalanceFloat = '%.3g' % groupBalance
    groupAccount.balanceVerified = bool(abs(groupBalance) < 1e-9)
    groupAccount.myBalanceFloat = UserProfile.getBalance(groupAccount.id, myUserProfile.id)
    groupAccount.myBalance = '%.2f' % groupAccount.myBalanceFloat
    return groupAccount