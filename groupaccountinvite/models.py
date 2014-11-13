from userprofile.models import UserProfile
from groupaccount.models import GroupAccount

from datetime import datetime
from itertools import chain

from django.db import models

import logging
logger = logging.getLogger(__name__)


class GroupAccountInvite(models.Model):
    groupAccount = models.ForeignKey(GroupAccount)
    inviter = models.ForeignKey(UserProfile, related_name='inviter')
    invitee = models.ForeignKey(UserProfile, related_name='invitee')
    isAccepted = models.BooleanField(default=False)
    isDeclined = models.BooleanField(default=False)
    createdDateAndTime = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    @staticmethod
    def get_invites_sent(userProfile):
        return GroupAccountInvite.objects.filter(inviter=userProfile)

    @staticmethod
    def get_invites_received(userProfile):
        return GroupAccountInvite.objects.filter(invitee=userProfile)

    @staticmethod
    def get_invites_sorted_by_date(userProfile):
        invitesSent = GroupAccountInvite.get_invites_sent(userProfile);
        invitesReceived = GroupAccountInvite.get_invites_received(userProfile);
        invitesAll = list(chain(invitesSent, invitesReceived))
        invitesAll = set(invitesAll)
        return sorted(invitesAll, key=lambda instance: instance.createdDateAndTime, reverse=True)

    def __str__(self):
        return self.groupAccount.name
