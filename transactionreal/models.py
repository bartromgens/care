from django.db import models

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class TransactionReal(models.Model):
  amount = models.FloatField('amount')
  sender = models.ForeignKey(UserProfile, related_name='sender')
  receiver = models.ForeignKey(UserProfile, related_name='receiver')
  comment = models.CharField(max_length=200)
  groupAccount = models.ForeignKey(GroupAccount)
  date = models.DateTimeField('date')
  
  def __unicode__(self):
    return self.comment