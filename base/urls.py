from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import admin
from base.views import HomeView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^care/$', login_required(HomeView.as_view())),
  url(r'^login/$', 'base.views.login'),
  url(r'^logout/$', 'base.views.logout'),
  url(r'^register/$', 'base.views.register'),
  url(r'^accounts/login/$', 'base.views.login'),
  url(r'^accounts/new/$', 'base.views.newGroup'),
  
  url(r'^transactions/', include('transaction.urls')),
  #url(r'^accounts/', include('accounts.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
