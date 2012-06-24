from itertools import chain
from django.template import RequestContext
from django.shortcuts import render_to_response

from base.views import BaseView
from groupaccount.models import GroupAccount
from groupaccountinvite.models import GroupAccountInvite
from groupaccountinvite.forms import NewInviteForm
from userprofile.models import UserProfile

class MyGroupAccountInvitesView(BaseView):
  template_name = "groupaccountinvite/overview.html"
  context_object_name = "my invites"

  def getSentInvites(self, userID):
    invites = GroupAccountInvite.objects.filter(inviter__id=userID)
    return invites
  
  def getReceivedInvites(self, userID):
    invitees = GroupAccountInvite.objects.filter(invitee__id=userID)
    return invitees
  
  def getNumberOfInvites(self, buyerId):
    invite = GroupAccountInvite.objects.all()
    return len(invite)
  
  def get_context_data(self, **kwargs):
    context = super(MyGroupAccountInvitesView, self).get_context_data(**kwargs)
    user = self.request.user
    
    invitesSent = self.getSentInvites(user.id)
    invitesReceived = self.getReceivedInvites(user.id)
#    invites = list(chain(invitesSent, invitesReceived))

    context['invitesSent'] = invitesSent
    context['invitesReceived'] = invitesReceived
    context['groupssection'] = True
    return context


class AcceptInviteView(MyGroupAccountInvitesView):
  template_name = "groupaccountinvite/overview.html"
  context_object_name = "my invites"

  def get_context_data(self, **kwargs):
    context = super(AcceptInviteView, self).get_context_data(**kwargs)
    user = self.request.user
    self.logger.warning("accepted " + self.kwargs['inviteId'])
    invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
    groupAccount = GroupAccount.objects.get(id=invite.groupAccount.id)
    invite.isAccepted = True
    invite.isDeclined = False
    userProfile = UserProfile.objects.get(user=user)
    userProfile.groupAccounts.add(groupAccount)
    userProfile.save()
    invite.save()
    
    self.logger.warning(userProfile.groupAccounts.all())
    invitesSent = self.getSentInvites(user.id)
    invitesReceived = self.getReceivedInvites(user.id)
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
    self.logger.warning("declined " + self.kwargs['inviteId'])
    invite = GroupAccountInvite.objects.get(id=self.kwargs['inviteId'])
    invite.isAccepted = False
    invite.isDeclined = True
    user = self.request.user
    groupAccount = GroupAccount.objects.get(id=invite.groupAccount.id)
    userProfile = UserProfile.objects.get(user=user)
    userProfile.groupAccounts.remove(groupAccount)
    userProfile.save()
    invite.save()
    
    invitesSent = self.getSentInvites(user.id)
    invitesReceived = self.getReceivedInvites(user.id)
    invites = list(chain(invitesSent, invitesReceived))

    context['invites'] = invites
    context['groupssection'] = True
    return context
  
  
def newInvite(request):
  def errorHandle(error):
    kwargs = {'user' : UserProfile.objects.get(user=request.user)}
    form = NewInviteForm(**kwargs)
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      context['groupssection'] = True
    return render_to_response('groupaccountinvite/new.html', context)
          
  if request.method == 'POST': # If the form has been submitted...
    kwargs = {'user' : UserProfile.objects.get(user=request.user)}
    form = NewInviteForm(request.POST, **kwargs) # A form bound to the POST data
    
    if form.is_valid(): # All validation rules pass
      form.save()
      context = RequestContext(request)

      if request.user.is_authenticated():
        context['user'] = request.user
        context['isLoggedin'] = True
        context['groupssection'] = True

      return render_to_response('groupaccountinvite/new.html', context)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  
  else:
    kwargs = {'user' : UserProfile.objects.get(user=request.user)}
    form = NewInviteForm(**kwargs) # An unbound form
    context = RequestContext(request)
    context['form'] = form
    context['groupssection'] = True
    
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
    return render_to_response('groupaccountinvite/new.html', context)