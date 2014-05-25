from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from groupaccount.views import GroupsView, MyGroupAccountsView, NewGroupAccountView, SucessNewGroupAccountView

urlpatterns = patterns('',
    url(r'^$', login_required(GroupsView.as_view())),
    url(r'^my', login_required(MyGroupAccountsView.as_view())),
    url(r'^new/$', login_required(NewGroupAccountView.as_view())),
    url(r'^new/success/$', login_required(SucessNewGroupAccountView.as_view())),
)
