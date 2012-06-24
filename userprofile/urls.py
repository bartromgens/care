from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from userprofile.views import EditUserProfileView, SuccessEditUserProfileView

urlpatterns = patterns('',
#  url(r'^$', login_required(EditUserProfileView.as_view())),
  url(r'^edit/(?P<pk>\d+)/$', login_required(EditUserProfileView.as_view(success_url="/userprofile/edit/success/"))),
  url(r'^edit/success/$', login_required(SuccessEditUserProfileView.as_view())),
)

urlpatterns += staticfiles_urlpatterns()