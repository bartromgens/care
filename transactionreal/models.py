from datetime import datetime
from itertools import chain

from django.db import models

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile


class TransactionReal(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    sender = models.ForeignKey(UserProfile, related_name='sender')
    receiver = models.ForeignKey(UserProfile, related_name='receiver')
    comment = models.CharField(max_length=200)
    group_account = models.ForeignKey(GroupAccount)
    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    def get_datetime_last_modified(self):
        from transaction.models import Modification
        modifications = Modification.objects.filter(transaction_real=self)
        if modifications.exists():
            modification = modifications.latest('date')
            return modification.date
        else:
            return self.date

    @staticmethod
    def get_transactions_real_sent(sender_id):
        transactions = TransactionReal.objects.filter(sender__id=sender_id).order_by("-date")
        for transaction in transactions:
            transaction.amountPerPerson = '%.2f' % transaction.amount
            transaction.amountPerPersonFloat = float(transaction.amount)
        return transactions

    @staticmethod
    def get_transactions_real_received(receiver_id):
        transactions = TransactionReal.objects.filter(receiver__id=receiver_id).order_by("-date")
        for transaction in transactions:
            transaction.amountPerPerson = '%.2f' % transaction.amount
            transaction.amountPerPersonFloat = float(transaction.amount)
        return transactions

    @staticmethod
    def get_transactions_real_sorted_by_last_modified(userprofile_id):
        sent_transactions = TransactionReal.get_transactions_real_sent(userprofile_id)
        received_transactions = TransactionReal.get_transactions_real_received(userprofile_id)
        transactions_real_all = list(chain(sent_transactions, received_transactions))
        for transaction in transactions_real_all:
            transaction.lastModified = transaction.get_datetime_last_modified();
        return sorted(transactions_real_all, key=lambda instance: instance.lastModified, reverse=True)

    def __str__(self):
        return self.comment
