from django.db import models

from userprofile.models import UserProfile
from groupaccount.models import GroupAccount

from datetime import datetime
# Create your models here.

class GroupAccountInvite(models.Model):
  groupAccount = models.ForeignKey(GroupAccount)
  inviter = models.ForeignKey(UserProfile, related_name='inviter')
  invitee = models.ForeignKey(UserProfile, related_name='invitee')
  isAccepted = models.BooleanField(default=False)
  isDeclined = models.BooleanField(default=False)
  createdDateAndTime = models.DateTimeField(default=datetime.now, editable=True, blank=True)

  def __unicode__(self):
    return self.groupAccount.name