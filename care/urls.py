from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from registration.forms import RegistrationFormUniqueEmail

from care.base.views import HomeView, AboutView, HelpView, NewRegistrationView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = [
  url(r'^$', login_required(HomeView.as_view())),
  url(r'^help/$', HelpView.as_view()),
  url(r'^about/$', AboutView.as_view()),

  url(r'^transactions/', include('care.transaction.urls')),
  url(r'^invites/', include('care.groupaccountinvite.urls')),
  url(r'^userprofile/', include('care.userprofile.urls')),
  url(r'^admin/', include(admin.site.urls)),

  url(r'^group/', include('care.groupaccount.urls')),
  url(r'^accounts/register/', NewRegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'), # include before the simple.urls to override register url

#  url(r'^accounts/reset/$', 'userprofile.views.password_reset_custom', name='password_reset'),
  url(r'^accounts/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
      'userprofile.views.password_reset_confirm_custom', name='password_reset_confirm'),

  url(r'^accounts/', include('registration.backends.simple.urls')),  # the django-registration module
]
