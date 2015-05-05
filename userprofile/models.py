from datetime import date, timedelta
import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from registration.signals import user_registered

from groupaccount.models import GroupAccount
import base.emailserver as emailserver


#users = User.objects.filter(groups__name='monkeys')


def create_userprofile(sender, user, request, **kwargs):
    logger.debug('signal create_userprofile()')
    profile = UserProfile(user=user, displayname=user.username)
    if NotificationInterval.objects.get(name="Monthly"):
        profile.historyEmailInterval = NotificationInterval.objects.get(name="Monthly")
    profile.save()
    emailserver.send_welcome_email(user.username, user.email)

# create a new userprofile when a user registers
user_registered.connect(create_userprofile)


class NotificationInterval(models.Model):
    name = models.CharField(max_length=100, unique=True)
    days = models.IntegerField()

    def __str__(self):
        return str(self.name)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    displayname = models.CharField(max_length=15, validators=[RegexValidator(r"^\S.*\S$|^\S$|^$", "This field cannot start or end with spaces.")])
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    group_accounts = models.ManyToManyField(GroupAccount, blank=True)
    showTableView = models.BooleanField(default=False)
    historyEmailInterval = models.ForeignKey(NotificationInterval, null=True)

    def __str__(self):
        return str(self.displayname)

    def get_show_table(self, doShowTable):
        if int(doShowTable) == 1 and self.showTableView:
            self.showTableView = False
            self.save()
        if int(doShowTable) == 2 and not self.showTableView:
            self.showTableView = True
            self.save()

    def send_transaction_history(self, force_send=False):
        if self.historyEmailInterval.days == 0 and not force_send:
            return # do not send anything when it is not forced and user set to 0 days
        date_end = date.today()
        date_start = date_end - timedelta(self.historyEmailInterval.days)
        import base.mailnotification as mailnotification
        transactionTableHtml = mailnotification.create_transaction_history_table_html(self, date_start, date_end)
        transactionRealTable = mailnotification.create_transaction_real_history_table_html(self, date_start, date_end)

        if transactionTableHtml == '' and transactionRealTable == '':
            return
        emailserver.send_transaction_history(self.user.username, self.user.email, transactionTableHtml, transactionRealTable, date_start, date_end)        

    @staticmethod
    def get_balance(groupAccountId, userProfileId):
        from transaction.models import Transaction
        from transactionreal.models import TransactionReal
        buyerTransactions = Transaction.objects.filter(groupAccount__id=groupAccountId, buyer__id=userProfileId)
        consumerTransactions = Transaction.objects.filter(groupAccount__id=groupAccountId, consumers__id=userProfileId)

        senderRealTransactions = TransactionReal.objects.filter(groupAccount__id=groupAccountId, sender__id=userProfileId)
        receiverRealTransactions = TransactionReal.objects.filter(groupAccount__id=groupAccountId, receiver__id=userProfileId)

        totalBought = 0.0
        totalConsumed = 0.0
        totalSent = 0.0
        totalReceived = 0.0

        for transaction in buyerTransactions:
            totalBought += float(transaction.amount)

        for transaction in consumerTransactions:
            nConsumers = transaction.consumers.count()
            totalConsumed += float(transaction.amount) / nConsumers

        for transaction in senderRealTransactions:
            totalSent += float(transaction.amount)

        for transaction in receiverRealTransactions:
            totalReceived += float(transaction.amount)

        balance = (totalBought + totalSent - totalConsumed - totalReceived)
        return balance
