from itertools import chain

from base.views import BaseView
from groupaccountinvite.models import GroupAccountInvite

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
  