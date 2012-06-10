from django.db import models
#import datetime
#from django.utils import timezone

#from django.contrib.auth.models import User

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile
#users = User.objects.filter(groups__name='monkeys')

class Transaction(models.Model):
  amount = models.FloatField('amount')
  what = models.CharField(max_length=200)
  buyer = models.ForeignKey(UserProfile, related_name='buyer')
  consumers = models.ManyToManyField(UserProfile, related_name='consumers')
  groupAccount = models.ForeignKey(GroupAccount)
  date = models.DateTimeField('date')
  
  def __unicode__(self):
    return self.what