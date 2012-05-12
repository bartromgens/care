from django.db import models
import datetime
from django.utils import timezone
from groupaccount.models import GroupAccount

from django.contrib.auth.models import User, Group

#users = User.objects.filter(groups__name='monkeys')

class UserProfile(models.Model):
  user = models.ForeignKey(User)
  groupAccounts = models.ManyToManyField(GroupAccount)
  #settings = models.ForeignKey(UserSettings)
  
  def __unicode__(self):
    return self.user.username