from groupaccount.models import GroupAccount

from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered  

import logging
logger = logging.getLogger(__name__)
 
#users = User.objects.filter(groups__name='monkeys')

def createUserProfile(sender, user, request, **kwargs):
  logger.debug('signal createUserProfile()')
  profile = UserProfile(user=user, displayname=user.username)
  profile.save()

user_registered.connect(createUserProfile)

class UserProfile(models.Model):
  user = models.ForeignKey(User)
  displayname = models.CharField(max_length=200)
  groupAccounts = models.ManyToManyField(GroupAccount)
  #settings = models.ForeignKey(UserSettings)
  
  def __unicode__(self):
    return self.displayname