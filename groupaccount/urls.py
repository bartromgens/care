from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from groupaccount.views import MyGroupAccountsView, NewGroupAccountView, SucessNewGroupAccountView, EditGroupSettingView

urlpatterns = patterns('',
    url(r'^my/(?P<tableView>\d+)$', login_required(MyGroupAccountsView.as_view())),
    url(r'^new/$', login_required(NewGroupAccountView.as_view())),
    url(r'^new/success/$', login_required(SucessNewGroupAccountView.as_view())),
    url(r'^settings/(?P<group_id>\d+)$', login_required(EditGroupSettingView.as_view())),
)
