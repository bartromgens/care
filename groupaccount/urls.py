from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from groupaccount.views import GroupsView, AccountDetailView, MyGroupsView

urlpatterns = patterns('',
    url(r'^$', login_required(GroupsView.as_view())),
    url(r'^my', login_required(MyGroupsView.as_view())),
    url(r'^(?P<accountId>\d+)/$', login_required(AccountDetailView.as_view())),
)