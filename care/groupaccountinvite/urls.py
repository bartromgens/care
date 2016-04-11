from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from care.groupaccountinvite.views import MyGroupAccountInvitesView, AcceptInviteView, DeclineInviteView, NewInviteView

urlpatterns = [
    url(r'^$', login_required(MyGroupAccountInvitesView.as_view())),
    url(r'^new/(?P<userProfileId>\d+)$', login_required(NewInviteView.as_view())),
    url(r'^accept/(?P<inviteId>\d+)/$', login_required(AcceptInviteView.as_view())),
    url(r'^decline/(?P<inviteId>\d+)/$', login_required(DeclineInviteView.as_view())),
]
