from django.db import models

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
  date = models.DateTimeField(auto_now=True, auto_now_add=True)
  
  def __unicode__(self):
    return self.what