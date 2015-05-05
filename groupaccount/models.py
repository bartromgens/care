from django.db import models

#users = User.objects.filter(groups__name='monkeys')


class GroupSetting(models.Model):
    notification_lower_limit = models.IntegerField(default=-100) # the lower limit on the balance a user can have in this group before a notification will be sent.
    notification_lower_limit_interval = models.ForeignKey('userprofile.NotificationInterval', null=True) # the balance notification interval in days
    
    def __str__(self):
        return 'id: ' + str(self.id) + ', limit: ' + str(self.notification_lower_limit) + ', interval: ' + str(self.notification_lower_limit_interval.name) 


class GroupAccount(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)
    settings = models.ForeignKey(GroupSetting, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def add_groupaccount_info(group_account, my_user_profile):
        from userprofile.models import UserProfile

        group_balance = 0.0
        group_account.userProfiles = UserProfile.objects.filter(group_accounts=group_account)
        for userProfile in group_account.userProfiles:
            userProfile.balanceFloat = UserProfile.get_balance(group_account.id, userProfile.id)
            userProfile.balance = '%.2f' % userProfile.balanceFloat
            group_balance += userProfile.balanceFloat
        group_account.groupBalance = '%.2f' % group_balance
        group_account.groupBalanceFloat = '%.3g' % group_balance
        group_account.balanceVerified = bool(abs(group_balance) < 1e-9)
        group_account.myBalanceFloat = UserProfile.get_balance(group_account.id, my_user_profile.id)
        group_account.myBalance = '%.2f' % group_account.myBalanceFloat
        return group_account
    