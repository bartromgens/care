from base.views import BaseView
from groupaccount.models import GroupAccount
from groupaccountinvite.models import GroupAccountInvite
from groupaccountinvite.forms import NewInviteForm
from userprofile.models import UserProfile

from itertools import chain
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)


class MyGroupAccountInvitesView(BaseView):
  template_name = "groupaccountinvite/overview.html"
  context_object_name = "my invites"

  def getActiveMenu(self):
    return 'invites'
  
  def getSentInvites(self, user):
    logger.debug('user.id: ' + str(user.id))
    userProfile = UserProfile.objects.get(user=user)
    invites = GroupAccountInvite.objects.filter(inviter=userProfile)
    return invites
  
  def getReceivedInvites(self, user):
    userProfile = UserProfile.objects.get(user=user)
    invitees = GroupAccountInvite.objects.filter(invitee=userProfile)
    return invitees
  
  def getNumberOfInvites(self, buyerId):
    invite = GroupAccountInvite.objects.all()
    return len(invite)
  
  def get_context_data(self, **kwargs):
    context = super(MyGroupAccountInvitesView, self).get_context_data(**kwargs)
    user = self.request.user
    
    invitesSent = self.getSentInvites(user).order_by('-createdDateAndTime')
    logger.debug(str(len(invitesSent)))
    invitesReceived = self.getReceivedInvites(user).order_by('-createdDateAndTime')
#    invites = list(chain(invitesSent, invitesReceived))

    context['invitesSent'] = invitesSent
    context['invitesReceived'] = invitesReceived
    return context


class AcceptInviteView(MyGroupAccountInvitesView):
  template_name = "groupaccountinvite/overview.html"
  context_object_name = "my invites"

  def get_context_data(self, **kwargs):
    context = super(AcceptInviteView, self).get_context_data(**kwargs)
    user = self.request.user
    logger.warning("accepted " + self.kwargs['inviteId'])
    invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
    groupAccount = GroupAccount.objects.get(id=invite.groupAccount.id)
    invite.isAccepted = True
    invite.isDeclined = False
    userProfile = UserProfile.objects.get(user=user)
    userProfile.groupAccounts.add(groupAccount)
    userProfile.save()
    invite.save()
    
    invitesSent = self.getSentInvites(user)
    invitesReceived = self.getReceivedInvites(user)
    invites = list(chain(invitesSent, invitesReceived))

    context['invites'] = invites
    context['groupssection'] = True
    return context

  
class DeclineInviteView(MyGroupAccountInvitesView):
  template_name = "groupaccountinvite/overview.html"
  context_object_name = "my invites"

  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(DeclineInviteView, self).get_context_data(**kwargs)
    logger.warning("declined " + self.kwargs['inviteId'])
    invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
    user = self.request.user
    userProfile = UserProfile.objects.get(user=user)
    
    logger.debug( userProfile.groupAccounts.get(id=invite.groupAccount.id) )
    
    if userProfile.groupAccounts.get(id=invite.groupAccount.id):
      logger.debug( 'Group is already accepted. Groups cannot be removed.' )
      invite.isAccepted = False
      invite.isDeclined = True
    else:
      logger.debug( 'Group is declined.' )
      invite.isDeclined = True
      groupAccount = GroupAccount.objects.get(id=invite.groupAccount.id)
      userProfile = UserProfile.objects.get(user=user)
      userProfile.groupAccounts.remove(groupAccount)
      userProfile.save()
    
    invite.save()
    
    invitesSent = self.getSentInvites(user)
    invitesReceived = self.getReceivedInvites(user)
    invites = list(chain(invitesSent, invitesReceived))

    context['invites'] = invites
    context['groupssection'] = True
    return context


class NewInviteView(FormView, BaseView):
  template_name = 'groupaccountinvite/new.html'
  form_class = NewInviteForm
  success_url = '/invites/'
  
  def getActiveMenu(self):
    return 'invites'
    
  def get_form(self, form_class):
    return NewInviteForm(self.request.user, **self.get_form_kwargs())   
    
  def form_valid(self, form):
    logger.debug('NewInviteView::form_valid()')
    context = super(NewInviteView, self).form_valid(form)
    
    form.save()
    return context
  
  def form_invalid(self, form):
    logger.debug('NewInviteView::form_invalid()')
    context = super(NewInviteView, self).form_invalid(form)   
    return context
  
  def get_context_data(self, **kwargs):
    context = super(NewInviteView, self).get_context_data(**kwargs)
    
    form = NewInviteForm(self.request.user, **self.get_form_kwargs())
    context['form'] = form
    return context
  