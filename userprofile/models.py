from groupaccount.models import GroupAccount

from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered 

import logging
logger = logging.getLogger(__name__)
 
#users = User.objects.filter(groups__name='monkeys')

def createUserProfile(sender, user, request, **kwargs):
  logger.debug('signal createUserProfile()')
  profile = UserProfile(user=user, displayname=user.username)
  profile.save()

user_registered.connect(createUserProfile)

class UserProfile(models.Model):
  user = models.ForeignKey(User)
  displayname = models.CharField(max_length=200)
  groupAccounts = models.ManyToManyField(GroupAccount, blank=True)
  #settings = models.ForeignKey(UserSettings)
  
  def __unicode__(self):
    return str(self.displayname)
  
  @staticmethod
  def getBalance(groupAccountId, userProfileId):
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
      totalBought += transaction.amount
      
    for transaction in consumerTransactions:
      nConsumers = transaction.consumers.count()
      totalConsumed += transaction.amount / nConsumers
      
    for transaction in senderRealTransactions:
      totalSent += transaction.amount
      
    for transaction in receiverRealTransactions:
      totalReceived += transaction.amount
      
    balance = (totalBought + totalSent - totalConsumed - totalReceived)
    return balance
