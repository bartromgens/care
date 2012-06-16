from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from groupaccount.views import GroupsView, AccountDetailView, MyGroupAccountsView

urlpatterns = patterns('',
    url(r'^$', login_required(GroupsView.as_view())),
    url(r'^my', login_required(MyGroupAccountsView.as_view())),
    url(r'^(?P<groupAccountId>\d+)/$', login_required(AccountDetailView.as_view())),
)
