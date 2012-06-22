from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from groupaccountinvite.views import MyGroupAccountInvitesView

urlpatterns = patterns('',
    url(r'^$', login_required(MyGroupAccountInvitesView.as_view())),
)
