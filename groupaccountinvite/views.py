from itertools import chain
from django.template import RequestContext
from django.shortcuts import render_to_response

from base.views import BaseView
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
    # Call the base implementation first to get a context
    context = super(MyGroupAccountInvitesView, self).get_context_data(**kwargs)
    user = self.request.user
    
    invitesSent = self.getSentInvites(user.id)
    invitesReceived = self.getReceivedInvites(user.id)
    invites = list(chain(invitesSent, invitesReceived))

    context['invites'] = invites
    context['groupssection'] = True
    return context# Create your views here.
  
  
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