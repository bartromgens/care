from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

from django.db import models

from itertools import chain
from datetime import datetime

# users = User.objects.filter(groups__name='monkeys')


class Modification(models.Model):
  user = models.ForeignKey(UserProfile, blank=True)
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  

class Transaction(models.Model):
  amount = models.DecimalField(max_digits=6, decimal_places=2)
  what = models.CharField(max_length=24)
  buyer = models.ForeignKey(UserProfile, related_name='buyer')
  consumers = models.ManyToManyField(UserProfile, related_name='consumers')
  groupAccount = models.ForeignKey(GroupAccount)
  comment = models.CharField(max_length=200,  blank=True)
  modifications = models.ManyToManyField(Modification, blank=True)
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
  @staticmethod
  def getBuyerTransactions(buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId).order_by("date")
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % float(transaction.amount)
      transaction.amountPerPersonFloat = float(transaction.amount)
    return transactions
  
  @staticmethod  
  def getConsumerTransactions(consumerId):
    transactions = Transaction.objects.filter(consumers__id=consumerId).order_by("date")
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % (-1*float(transaction.amount)/transaction.consumers.count())
      transaction.amountPerPersonFloat = (-1*float(transaction.amount)/transaction.consumers.count())
    return transactions
  
  @staticmethod
  def getTransactionsAllSortedByDate(userProfileId):
    buyerTransactions = Transaction.getBuyerTransactions(userProfileId)
    consumerTransactions = Transaction.getConsumerTransactions(userProfileId)
    transactionsAll = list(chain(buyerTransactions, consumerTransactions))
    return sorted(transactionsAll, key=lambda instance: instance.date, reverse=True)
  
  def __str__(self):
    return self.what
  