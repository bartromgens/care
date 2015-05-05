from datetime import datetime
from itertools import chain

from django.db import models

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile
from transactionreal.models import TransactionReal

# users = User.objects.filter(groups__name='monkeys')


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    what = models.CharField(max_length=24)
    buyer = models.ForeignKey(UserProfile, related_name='buyer')
    consumers = models.ManyToManyField(UserProfile, related_name='consumers')
    group_account = models.ForeignKey(GroupAccount)
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    def get_datetime_last_modified(self):
        modifications = Modification.objects.filter(transaction=self)
        if modifications.exists():
            modification = modifications.latest('date')
            return modification.date
        else:
            return self.date

    @staticmethod
    def get_buyer_transactions(buyerId):
        transactions = Transaction.objects.filter(buyer__id=buyerId).order_by("-date")
        for transaction in transactions:
            transaction.amountPerPerson = '%.2f' % float(transaction.amount)
            transaction.amountPerPersonFloat = float(transaction.amount)
        return transactions

    @staticmethod
    def get_consumer_transactions(consumer_id):
        transactions = Transaction.objects.filter(consumers__id=consumer_id).order_by("-date")
        for transaction in transactions:
            transaction.amountPerPerson = '%.2f' % (-1*float(transaction.amount)/transaction.consumers.count())
            transaction.amountPerPersonFloat = (-1*float(transaction.amount)/transaction.consumers.count())
        return transactions

    @staticmethod
    def get_transactions_sorted_by_last_modified(userProfileId):
        buyer_transactions = Transaction.get_buyer_transactions(userProfileId)
        consumer_transactions = Transaction.get_consumer_transactions(userProfileId)
        transactions_all = list(chain(buyer_transactions, consumer_transactions))
        for transaction in transactions_all:
            transaction.lastModified = transaction.get_datetime_last_modified()
        return sorted(transactions_all, key=lambda instance: instance.lastModified, reverse=True)

    def __str__(self):
        return self.what


class Modification(models.Model):
    user = models.ForeignKey(UserProfile, blank=True)
    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
    transaction = models.ForeignKey(Transaction, blank=True, null=True)
    transaction_real = models.ForeignKey(TransactionReal, blank=True, null=True)
