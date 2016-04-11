
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from care.userprofile.views import SendMyTransactionHistory
from care.userprofile.views import EditUserProfileView
from care.userprofile.views import SuccessEditUserProfileView
from care.userprofile.views import SearchUserProfileView


urlpatterns = [
  url(r'^edit/$', login_required(EditUserProfileView.as_view(success_url="/userprofile/edit/success/"))),
  url(r'^edit/success/$', login_required(SuccessEditUserProfileView.as_view())),
  url(r'^search/$', login_required(SearchUserProfileView.as_view())),
  url(r'^sendmyhistory/$', login_required(SendMyTransactionHistory.as_view())),
]

urlpatterns += staticfiles_urlpatterns()
