from django.db import models
from groupaccount.models import GroupAccount

from django.contrib.auth.models import User

#users = User.objects.filter(groups__name='monkeys')

class UserProfile(models.Model):
  user = models.ForeignKey(User)
  displayname = models.CharField(max_length=200)
  groupAccounts = models.ManyToManyField(GroupAccount)
  #settings = models.ForeignKey(UserSettings)
  
  def __unicode__(self):
    return self.displayname