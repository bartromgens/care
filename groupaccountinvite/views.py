from base.views import BaseView
from groupaccount.models import GroupAccount
from groupaccountinvite.models import GroupAccountInvite
from groupaccountinvite.forms import NewInviteForm
from userprofile.models import UserProfile
from base import emailserver

from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)


class MyGroupAccountInvitesView(BaseView):
    template_name = "groupaccountinvite/overview.html"
    context_object_name = "my invites"

    def get_active_menu(self):
        return 'invites'

    def get_number_of_invites(self, buyerId):
        invite = GroupAccountInvite.objects.all()
        return len(invite)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userProfile = self.get_userprofile()
        invites_sent = GroupAccountInvite.get_invites_sent(userProfile).order_by('-createdDateAndTime')
        invites_received = GroupAccountInvite.get_invites_received(userProfile).order_by('-createdDateAndTime')
#    invites = list(chain(invites_sent, invites_received))

        context['invites_sent'] = invites_sent
        context['invites_received'] = invites_received
        return context


class AcceptInviteView(MyGroupAccountInvitesView):
    template_name = "groupaccountinvite/overview.html"
    context_object_name = "my invites"

    def get_context_data(self, **kwargs):
        user = self.request.user
        logger.warning("accepted " + self.kwargs['inviteId'])
        invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
        # make sure accepter is the invitee
        if invite.invitee.user == user:
            group_account = GroupAccount.objects.get(id=invite.group_account.id)
            invite.isAccepted = True
            invite.isDeclined = False
            userProfile = self.get_userprofile()
            userProfile.group_accounts.add(group_account)
            userProfile.save()
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
        userProfile = UserProfile.objects.get(user=user)

        # make sure the decliner is the invitee
        if invite.invitee.user == user:
            if userProfile.group_accounts.filter(id=invite.group_account.id):
                logger.warning( 'Group is already accepted. Groups cannot be removed.' )
                invite.isAccepted = False
                invite.isDeclined = True
            else:
                logger.debug( 'Group is declined.' )
                invite.isDeclined = True
                group_account = GroupAccount.objects.get(id=invite.group_account.id)
                userProfile = UserProfile.objects.get(user=user)
                userProfile.group_accounts.remove(group_account)
                userProfile.save()
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
        userProfileToInvite = UserProfile.objects.get(id=self.kwargs['userProfileId'])
        form = NewInviteForm(self.request.user, userProfileToInvite, **self.get_form_kwargs())
        return form

    def form_valid(self, form):
        logger.debug('NewInviteView::form_valid()')
        context = super().form_valid(form)
        invite = form.save()
        emailserver.send_invite_email(self.request.user.username, invite.invitee.user.username, invite.group_account.name, invite.invitee.user.email)
        return context

    def form_invalid(self, form):
        logger.debug('NewInviteView::form_invalid()')
        context = super().form_invalid(form)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userProfileToInvite = UserProfile.objects.get(id=self.kwargs['userProfileId'])
        form = NewInviteForm(self.request.user, userProfileToInvite, **self.get_form_kwargs())
        context['form'] = form
        return context
