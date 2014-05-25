from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from base.views import HomeView, AboutView, HelpView, NewRegistrationView 

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
  
  url(r'^accounts/', include('groupaccount.urls')),
  url(r'^accounts/', include('registration.backends.simple.urls')), # the django-registration module
  url(r'^accounts/register/', NewRegistrationView.as_view()),
)
