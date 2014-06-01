from django.db import models

# from django.contrib.auth.models import User

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

from datetime import datetime

# users = User.objects.filter(groups__name='monkeys')

class Transaction(models.Model):
  amount = models.DecimalField(max_digits=6, decimal_places=2)
  what = models.CharField(max_length=24)
  buyer = models.ForeignKey(UserProfile, related_name='buyer')
  consumers = models.ManyToManyField(UserProfile, related_name='consumers')
  groupAccount = models.ForeignKey(GroupAccount)
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
  @staticmethod
  def getBuyerTransactions(buyerId):
    transactions = Transaction.objects.filter(buyer__id=buyerId).order_by("date")
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % (transaction.amount)
      transaction.amountPerPersonFloat = transaction.amount
    return transactions
  
  @staticmethod  
  def getConsumerTransactions(consumerId):
    transactions = Transaction.objects.filter(consumers__id=consumerId).order_by("date")
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % (-1*transaction.amount/transaction.consumers.count())
      transaction.amountPerPersonFloat = (-1*transaction.amount/transaction.consumers.count())
    return transactions
  
  def __str__(self):
    return self.what
