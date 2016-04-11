import logging
from datetime import datetime
from itertools import chain

from django.db import models

from care.groupaccount.models import GroupAccount
from care.userprofile.models import UserProfile

logger = logging.getLogger(__name__)


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
    def get_buyer_transactions(buyer_id):
        transactions = Transaction.objects.filter(buyer__id=buyer_id).order_by("-date").prefetch_related('modification', 'consumers', 'group_account')
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % float(transaction.amount)
            transaction.amount_per_person_float = float(transaction.amount)
        return transactions

    @staticmethod
    def get_consumer_transactions(consumer_id):
        transactions = Transaction.objects.filter(consumers__id=consumer_id).order_by("-date").prefetch_related('modification', 'consumers', 'group_account')
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % (-1*float(transaction.amount)/transaction.consumers.count())
            transaction.amount_per_person_float = (-1*float(transaction.amount)/transaction.consumers.count())
        return transactions

    @staticmethod
    def get_transactions_sorted_by_last_modified(userprofile_id):
        buyer_transactions = Transaction.get_buyer_transactions(userprofile_id)
        consumer_transactions = Transaction.get_consumer_transactions(userprofile_id)
        transactions_all = list(chain(buyer_transactions, consumer_transactions))
        for transaction in transactions_all:
            transaction.last_modified = transaction.get_datetime_last_modified()
            transaction.modifications = Modification.objects.filter(transaction=transaction)
        return sorted(transactions_all, key=lambda instance: instance.last_modified, reverse=True)

    def __str__(self):
        return self.what


class TransactionReal(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    sender = models.ForeignKey(UserProfile, related_name='sender')
    receiver = models.ForeignKey(UserProfile, related_name='receiver')
    comment = models.CharField(max_length=200)
    group_account = models.ForeignKey(GroupAccount)
    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    def get_datetime_last_modified(self):
        modifications = Modification.objects.filter(transaction_real=self)
        if modifications.exists():
            modification = modifications.latest('date')
            return modification.date
        else:
            return self.date

    @staticmethod
    def get_transactions_real_sent(sender_id):
        transactions = TransactionReal.objects.filter(sender__id=sender_id).prefetch_related('modification', 'sender', 'receiver').order_by("-date")
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % transaction.amount
            transaction.amount_per_person_float = float(transaction.amount)
        return transactions

    @staticmethod
    def get_transactions_real_received(receiver_id):
        transactions = TransactionReal.objects.filter(receiver__id=receiver_id).prefetch_related('modification', 'sender', 'receiver').order_by("-date")
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % transaction.amount
            transaction.amount_per_person_float = float(transaction.amount)
        return transactions

    @staticmethod
    def get_transactions_real_sorted_by_last_modified(userprofile_id):
        sent_transactions = TransactionReal.get_transactions_real_sent(userprofile_id)
        received_transactions = TransactionReal.get_transactions_real_received(userprofile_id)
        transactions_real_all = list(chain(sent_transactions, received_transactions))
        for transaction_real in transactions_real_all:
            transaction_real.last_modified = transaction_real.get_datetime_last_modified()
            transaction_real.modifications = Modification.objects.filter(transaction_real=transaction_real)
        return sorted(transactions_real_all, key=lambda instance: instance.last_modified, reverse=True)

    def __str__(self):
        return self.comment


class Modification(models.Model):
    user = models.ForeignKey(UserProfile, blank=True)
    date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
    transaction = models.ForeignKey(Transaction, blank=True, null=True, related_name='modification')
    transaction_real = models.ForeignKey(TransactionReal, blank=True, null=True, related_name='modification')
