from base.views import HomeView, AboutView, HelpView, NewRegistrationView 

from registration.forms import RegistrationFormUniqueEmail

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', login_required(HomeView.as_view())),
  url(r'^help/$', HelpView.as_view()),
  url(r'^about/$', AboutView.as_view()),
  
  url(r'^transactions/', include('transaction.urls')),
  url(r'^transactionsreal/', include('transactionreal.urls')),
  url(r'^invites/', include('groupaccountinvite.urls')),
  url(r'^userprofile/', include('userprofile.urls')),
  url(r'^admin/', include(admin.site.urls)),
  
  url(r'^group/', include('groupaccount.urls')),
  url(r'^accounts/register/', NewRegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'), # include before the simple.urls to override register url
  
#   url(r'^accounts/reset/$', 'userprofile.views.password_reset_custom', name='password_reset'),
  url(r'^accounts/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
      'userprofile.views.password_reset_confirm_custom', name='password_reset_confirm'),
  
  url(r'^accounts/', include('registration.backends.simple.urls')), # the django-registration module
)
