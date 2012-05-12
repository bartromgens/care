from django.db import models
import datetime
from django.utils import timezone

from django.contrib.auth.models import User

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile
#users = User.objects.filter(groups__name='monkeys')

class TransactionReal(models.Model):
  amount = models.FloatField('amount')
  sender = models.ForeignKey(UserProfile, related_name='sender')
  receiver = models.ForeignKey(UserProfile, related_name='receiver')
  comment = models.CharField(max_length=200)
  groupAccount = models.ForeignKey(GroupAccount)
  date = models.DateTimeField('date')
  
  def __unicode__(self):
    return self.what