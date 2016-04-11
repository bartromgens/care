from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from care.groupaccount.views import MyGroupAccountsView, NewGroupAccountView, SucessNewGroupAccountView, EditGroupSettingView

urlpatterns = [
    url(r'^my/(?P<tableView>\d+)$', login_required(MyGroupAccountsView.as_view())),
    url(r'^new/$', login_required(NewGroupAccountView.as_view())),
    url(r'^new/success/$', login_required(SucessNewGroupAccountView.as_view())),
    url(r'^settings/(?P<groupsettings_id>\d+)$', login_required(EditGroupSettingView.as_view())),
]
