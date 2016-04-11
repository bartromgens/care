from django.db import models

#users = User.objects.filter(groups__name='monkeys')


class GroupSetting(models.Model):
    notification_lower_limit = models.IntegerField(default=-100) # the lower limit on the balance a user can have in this group before a notification will be sent.
    notification_lower_limit_interval = models.ForeignKey('userprofile.NotificationInterval', null=True) # the balance notification interval in days
    
    def __str__(self):
        return 'id: ' + str(self.id) + ', limit: ' + str(self.notification_lower_limit)


class GroupAccount(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)
    settings = models.ForeignKey(GroupSetting, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def add_groupaccount_info(group_account, my_user_profile):
        from care.userprofile.models import UserProfile

        group_balance = 0.0
        group_account.user_profiles = UserProfile.objects.filter(group_accounts=group_account).prefetch_related('user')
        for user_profile in group_account.user_profiles:
            user_profile.balance_float = UserProfile.get_balance(group_account.id, user_profile.id)
            user_profile.balance = '%.2f' % user_profile.balance_float
            group_balance += user_profile.balance_float
        group_account.group_balance = '%.2f' % group_balance
        group_account.group_balance_float = '%.3g' % group_balance
        group_account.balance_verified = bool(abs(group_balance) < 1e-9)
        group_account.my_balance_float = UserProfile.get_balance(group_account.id, my_user_profile.id)
        group_account.my_balance = '%.2f' % group_account.my_balance_float
        return group_account
    