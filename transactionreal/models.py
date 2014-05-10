from django.db import models

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

from datetime import datetime

class TransactionReal(models.Model):
  amount = models.FloatField('amount')
  sender = models.ForeignKey(UserProfile, related_name='sender')
  receiver = models.ForeignKey(UserProfile, related_name='receiver')
  comment = models.CharField(max_length=200)
  groupAccount = models.ForeignKey(GroupAccount)
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
  def __unicode__(self):
    return self.comment