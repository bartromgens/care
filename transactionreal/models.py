from django.db import models

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile
from transaction.models import Modification

from itertools import chain
from datetime import datetime

class TransactionReal(models.Model):
  amount = models.DecimalField(max_digits=6, decimal_places=2)
  sender = models.ForeignKey(UserProfile, related_name='sender')
  receiver = models.ForeignKey(UserProfile, related_name='receiver')
  comment = models.CharField(max_length=200)
  groupAccount = models.ForeignKey(GroupAccount)
  modifications = models.ManyToManyField(Modification, blank=True)
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)

  def get_datetime_last_modified(self):
    if self.modifications.all():
      modification = self.modifications.latest('date')
      return modification.date
    else:
      return self.date
  
  @staticmethod
  def getSentTransactionsReal(senderId):
    transactions = TransactionReal.objects.filter(sender__id=senderId).order_by("-date")
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % transaction.amount
      transaction.amountPerPersonFloat = float(transaction.amount)
    return transactions
  
  @staticmethod  
  def getReceivedTransactionsReal(receiverId):
    transactions = TransactionReal.objects.filter(receiver__id=receiverId).order_by("-date")
    for transaction in transactions:
      transaction.amountPerPerson = '%.2f' % transaction.amount
      transaction.amountPerPersonFloat = float(transaction.amount)
    return transactions
  
  @staticmethod
  def getTransactionsRealAllSortedByDateLastModified(userProfileId):
    sentTransactions = TransactionReal.getSentTransactionsReal(userProfileId)
    receivedTransactions = TransactionReal.getReceivedTransactionsReal(userProfileId)
    transactionsRealAll = list(chain(sentTransactions, receivedTransactions))
    for transaction in transactionsRealAll:
      transaction.lastModified = transaction.get_datetime_last_modified();
    return sorted(transactionsRealAll, key=lambda instance: instance.lastModified, reverse=True)
    
  def __str__(self):
    return self.comment