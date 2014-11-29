from django.db import models

#users = User.objects.filter(groups__name='monkeys')

class GroupSetting(models.Model):
    notification_lower_limit = models.IntegerField(default=100) # the max negative balance a user can have in this group before a notification will be sent.
    notification_lower_limit_interval = models.ForeignKey('userprofile.NotificationInterval', null=True) # the negative balance notification interval in days
    
    def __str__(self):
        return 'id: ' + str(self.id) + ', limit: ' + str(self.notification_lower_limit) + ', interval: ' + str(self.notification_lower_limit_interval.name) 

class GroupAccount(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)
    settings = models.ForeignKey(GroupSetting, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def add_groupaccount_info(groupAccount, myUserProfile):
        from userprofile.models import UserProfile

        groupBalance = 0.0
        groupAccount.userProfiles = UserProfile.objects.filter(groupAccounts=groupAccount)
        for userProfile in groupAccount.userProfiles:
            userProfile.balanceFloat = UserProfile.get_balance(groupAccount.id, userProfile.id)
            userProfile.balance = '%.2f' % userProfile.balanceFloat
            groupBalance += userProfile.balanceFloat
        groupAccount.groupBalance = '%.2f' % groupBalance
        groupAccount.groupBalanceFloat = '%.3g' % groupBalance
        groupAccount.balanceVerified = bool(abs(groupBalance) < 1e-9)
        groupAccount.myBalanceFloat = UserProfile.get_balance(groupAccount.id, myUserProfile.id)
        groupAccount.myBalance = '%.2f' % groupAccount.myBalanceFloat
        return groupAccount
    