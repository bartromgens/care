from django.db import models
import datetime
from django.utils import timezone

from django.contrib.auth.models import User

#users = User.objects.filter(groups__name='monkeys')

class GroupAccount(models.Model):
  name = models.CharField(max_length=200)
  number = models.IntegerField(unique=True)
  #settings = models.ForeignKey(GroupSettings)
  
  def __unicode__(self):
    return self.name