from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from groupaccount.views import GroupsView, MyGroupAccountsView, NewGroupAccountView

urlpatterns = patterns('',
    url(r'^$', login_required(GroupsView.as_view())),
    url(r'^my', login_required(MyGroupAccountsView.as_view())),
    url(r'^new/$', login_required(NewGroupAccountView.as_view())),
    url(r'^newsucces/$', login_required(NewGroupAccountView.as_view())),
#     url(r'^(?P<groupAccountId>\d+)/$', login_required(MyTransactionView.as_view())),
)
