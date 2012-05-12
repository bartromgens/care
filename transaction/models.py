from django.db import models
import datetime
from django.utils import timezone

from django.contrib.auth.models import User

from groupaccount.models import GroupAccount
#users = User.objects.filter(groups__name='monkeys')

class Transaction(models.Model):
  amount = models.FloatField('amount')
  what = models.CharField(max_length=200)
  group = models.ForeignKey(GroupAccount)
  date = models.DateTimeField('date')
  buyer = models.ForeignKey(User, related_name='buyer')
  consumers = models.ManyToManyField(User, related_name='consumers')
  
  def __unicode__(self):
    return self.what