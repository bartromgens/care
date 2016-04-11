import logging
from datetime import datetime
from itertools import chain

from django.db import models

from care.userprofile.models import UserProfile
from care.groupaccount.models import GroupAccount

logger = logging.getLogger(__name__)


class GroupAccountInvite(models.Model):
    group_account = models.ForeignKey(GroupAccount)
    inviter = models.ForeignKey(UserProfile, related_name='inviter')
    invitee = models.ForeignKey(UserProfile, related_name='invitee')
    isAccepted = models.BooleanField(default=False)
    isDeclined = models.BooleanField(default=False)
    createdDateAndTime = models.DateTimeField(default=datetime.now, editable=True, blank=True)

    @staticmethod
    def get_invites_sent(userprofile):
        return GroupAccountInvite.objects.filter(inviter=userprofile)

    @staticmethod
    def get_invites_received(userprofile):
        return GroupAccountInvite.objects.filter(invitee=userprofile)

    @staticmethod
    def get_invites_sorted_by_date(userprofile):
        invites_sent = GroupAccountInvite.get_invites_sent(userprofile)
        invites_received = GroupAccountInvite.get_invites_received(userprofile)
        invites_all = list(chain(invites_sent, invites_received))
        invites_all = set(invites_all)
        return sorted(invites_all, key=lambda instance: instance.createdDateAndTime, reverse=True)

    def __str__(self):
        return self.group_account.name
