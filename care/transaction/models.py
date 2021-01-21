import logging
import datetime
from itertools import chain

from django.db import models
from django.db.models import Count, F, ExpressionWrapper
from django.core.exceptions import ValidationError

from care.fields.recurrencefield import RecurrenceField

from care.groupaccount.models import GroupAccount
from care.userprofile.models import UserProfile

logger = logging.getLogger(__name__)


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    what = models.CharField(max_length=24)
    buyer = models.ForeignKey(UserProfile, related_name='buyer', on_delete=models.PROTECT)
    consumers = models.ManyToManyField(UserProfile, related_name='consumers')
    group_account = models.ForeignKey(GroupAccount, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now,
                                editable=True, blank=True)

    def get_datetime_last_modified(self):
        if self.modifications.exists():
            return self.modifications.latest('date').date
        return self.date

    @staticmethod
    def get_buyer_transactions(buyer_id):
        transactions = (
            Transaction.objects
            .filter(buyer__id=buyer_id)
            .order_by("-date")
            .prefetch_related('modifications', 'group_account')
        )
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % float(transaction.amount)
            transaction.amount_per_person_float = float(transaction.amount)
        return transactions

    @staticmethod
    def get_consumer_transactions(consumer_id):
        transactions = (
            Transaction.objects
            .annotate(
                amount_per_person=ExpressionWrapper(
                    F('amount') / (1.0*Count('consumers')),
                    output_field=models.FloatField()
                )
            ).filter(consumers__id=consumer_id)
            .order_by("-date")
            .prefetch_related('modifications', 'group_account')
        )

        for transaction in transactions:
            transaction.amount_per_person_float = float((-1*transaction.amount_per_person))
            transaction.amount_per_person = '%.2f' % float(-1 * transaction.amount_per_person)
        return transactions

    @staticmethod
    def get_transactions_sorted_by_last_modified(userprofile_id):
        buyer_transactions = Transaction.get_buyer_transactions(userprofile_id)
        consumer_transactions = Transaction.get_consumer_transactions(userprofile_id)
        transactions_all = list(chain(buyer_transactions, consumer_transactions))
        for transaction in transactions_all:
            transaction.last_modified = transaction.get_datetime_last_modified()
        return sorted(transactions_all, key=lambda instance: instance.last_modified, reverse=True)

    def __str__(self):
        return self.what


class TransactionRecurring(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    what = models.CharField(max_length=24)
    buyer = models.ForeignKey(UserProfile, related_name='rec_buyer', on_delete=models.PROTECT)
    consumers = models.ManyToManyField(UserProfile,
                                       related_name='rec_consumers')
    group_account = models.ForeignKey(GroupAccount, on_delete=models.PROTECT)
    comment = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, editable=True,
                                blank=True)
    every = RecurrenceField()
    last_occurrence = models.DateTimeField(
        default=datetime.datetime.fromtimestamp(0),
        editable=False,
        blank=True)

    @property
    def next_due(self):
        ''' Get the next occurrence date for this recurring event '''
        not_before = datetime.datetime.combine(
            self.last_occurrence.date() + datetime.timedelta(days=1),
            datetime.time(0))

        return self.every.after(max(not_before, self.date))

    @property
    def period_str(self):
        ''' Get the textual description of the period '''
        descrs = []
        for rule in self.every.rrules:
            descrs.append(rule.to_text())
        return '; '.join(descrs)

    def create_occurrence(self):
        ''' Create an occurrence of this event and update it '''
        transaction = Transaction(
            amount=self.amount,
            what=self.what,
            buyer=self.buyer,
            group_account=self.group_account,
            comment=self.comment,
            date=datetime.datetime.now(),
        )
        try:
            transaction.full_clean()
        except ValidationError:
            return  # FIXME do something better

        transaction.save()
        for consumer in self.consumers.all():
            transaction.consumers.add(consumer)
        transaction.save()
        self.last_occurrence = datetime.datetime.now()
        self.save()

    def get_datetime_last_modified(self):
        if self.modifications.exists():
            return self.modifications.latest('date').date
        return self.date

    @staticmethod
    def get_buyer_transactions(buyer_id):
        transactions = TransactionRecurring.objects \
            .filter(buyer__id=buyer_id).order_by("-date") \
            .prefetch_related('modifications', 'group_account')
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % float(transaction.amount)
            transaction.amount_per_person_float = float(transaction.amount)
        return transactions

    @staticmethod
    def get_consumer_transactions(consumer_id):
        transactions = (
            TransactionRecurring.objects
            .annotate(
                amount_per_person=ExpressionWrapper(
                    F('amount') / (1.0*Count('consumers')),
                    output_field=models.FloatField())
            )
            .filter(consumers__id=consumer_id)
            .order_by("-date")
            .prefetch_related('modifications', 'group_account')
        )

        for transaction in transactions:
            transaction.amount_per_person_float = \
                float((-1*transaction.amount_per_person))
            transaction.amount_per_person = \
                '%.2f' % float(-1 * transaction.amount_per_person)
        return transactions

    @staticmethod
    def get_transactions_sorted_by_last_modified(userprofile_id):
        buyer_transactions = \
            TransactionRecurring.get_buyer_transactions(userprofile_id)
        consumer_transactions = \
            TransactionRecurring.get_consumer_transactions(userprofile_id)
        transactions_all = list(chain(buyer_transactions,
                                      consumer_transactions))
        for transaction in transactions_all:
            transaction.last_modified = \
                transaction.get_datetime_last_modified()
        return sorted(transactions_all,
                      key=lambda instance: instance.last_modified,
                      reverse=True)

    def __str__(self):
        return self.what


class TransactionReal(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    sender = models.ForeignKey(UserProfile, related_name='sender', on_delete=models.PROTECT)
    receiver = models.ForeignKey(UserProfile, related_name='receiver', on_delete=models.PROTECT)
    comment = models.CharField(max_length=200)
    group_account = models.ForeignKey(GroupAccount, on_delete=models.PROTECT)
    date = models.DateTimeField(default=datetime.datetime.now,
                                editable=True, blank=True)

    def get_datetime_last_modified(self):
        if self.modifications.exists():
            return self.modifications.latest('date').date
        return self.date

    @staticmethod
    def get_transactions_real_sent(sender_id):
        transactions = (
            TransactionReal.objects
            .filter(sender__id=sender_id)
            .order_by("-date")
            .prefetch_related('modifications', 'group_account')
        )
        for transaction in transactions:
            transaction.amount_per_person = '%.2f' % transaction.amount
            transaction.amount_per_person_float = float(transaction.amount)
        return transactions

    @staticmethod
    def get_transactions_real_received(receiver_id):
        transactions = (
            TransactionReal.objects
            .filter(receiver__id=receiver_id)
            .order_by("-date")
            .prefetch_related('modifications', 'group_account')
        )
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
        return sorted(transactions_real_all, key=lambda instance: instance.last_modified, reverse=True)

    def __str__(self):
        return self.comment


class Modification(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, on_delete=models.PROTECT)
    date = models.DateTimeField(default=datetime.datetime.now,
                                editable=True, blank=True)
    transaction = models.ForeignKey(Transaction, blank=True, null=True, related_name='modifications', on_delete=models.SET_NULL)
    transaction_real = models.ForeignKey(TransactionReal, blank=True, null=True,
                                         related_name='modifications',
                                         on_delete=models.SET_NULL)
    transaction_recurring = models.ForeignKey(TransactionRecurring,
                                              blank=True, null=True,
                                              related_name='modifications',
                                              on_delete=models.SET_NULL)
