from django.db import models

# from django.contrib.auth.models import User

from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

from datetime import datetime

# users = User.objects.filter(groups__name='monkeys')

class Transaction(models.Model):
  amount = models.DecimalField(max_digits=6, decimal_places=2)
  what = models.CharField(max_length=200)
  buyer = models.ForeignKey(UserProfile, related_name='buyer')
  consumers = models.ManyToManyField(UserProfile, related_name='consumers')
  groupAccount = models.ForeignKey(GroupAccount)
  date = models.DateTimeField(default=datetime.now, editable=True, blank=True)
  
  def __unicode__(self):
    return self.what
