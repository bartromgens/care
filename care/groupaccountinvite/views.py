from care.base.views import BaseView
from care.groupaccount.models import GroupAccount
from care.groupaccountinvite.models import GroupAccountInvite
from care. groupaccountinvite.forms import NewInviteForm
from care.userprofile.models import UserProfile
from care.base import emailserver

from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)


class MyGroupAccountInvitesView(BaseView):
    template_name = "groupaccountinvite/overview.html"
    context_object_name = "my invites"

    def get_active_menu(self):
        return 'invites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_userprofile()
        invites_sent = GroupAccountInvite.get_invites_sent(user_profile).order_by('-createdDateAndTime')
        invites_received = GroupAccountInvite.get_invites_received(user_profile).order_by('-createdDateAndTime')
        context['invites_sent'] = invites_sent
        context['invites_received'] = invites_received
        return context


class AcceptInviteView(MyGroupAccountInvitesView):
    template_name = "groupaccountinvite/overview.html"
    context_object_name = "my invites"

    def get_context_data(self, **kwargs):
        invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
        # make sure accepter is the invitee
        if invite.invitee.user == self.request.user:
            invite.isAccepted = True
            invite.isDeclined = False
            user_profile = self.get_userprofile()
            group_account = GroupAccount.objects.get(id=invite.group_account.id)
            user_profile.group_accounts.add(group_account)
            user_profile.save()
            invite.save()

        context = super().get_context_data(**kwargs)
        context['groupssection'] = True
        return context


class DeclineInviteView(MyGroupAccountInvitesView):
    template_name = "groupaccountinvite/overview.html"
    context_object_name = "my invites"

    def get_context_data(self, **kwargs):
        invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)

        # make sure the decliner is the invitee
        if invite.invitee.user == user:
            if user_profile.group_accounts.filter(id=invite.group_account.id):
                logger.warning( 'Group is already accepted. Groups cannot be removed.' )
                invite.isAccepted = False
                invite.isDeclined = True
            else:
                logger.debug( 'Group is declined.' )
                invite.isDeclined = True
                group_account = GroupAccount.objects.get(id=invite.group_account.id)
                user_profile = UserProfile.objects.get(user=user)
                user_profile.group_accounts.remove(group_account)
                user_profile.save()
            invite.save()

        context = super().get_context_data(**kwargs)
        context['groupssection'] = True
        return context


class NewInviteView(FormView, BaseView):
    template_name = 'groupaccountinvite/new.html'
    form_class = NewInviteForm
    success_url = '/invites/'

    def get_active_menu(self):
        return 'invites'

    def get_form(self, form_class=NewInviteForm):
        user_profile_to_invite = UserProfile.objects.get(id=self.kwargs['userProfileId'])
        form = NewInviteForm(self.request.user, user_profile_to_invite, **self.get_form_kwargs())
        return form

    def form_valid(self, form):
        context = super().form_valid(form)
        invite = form.save()
        emailserver.send_invite_email(self.request.user.username, invite.invitee.user.username, invite.group_account.name, invite.invitee.user.email)
        return context

