from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from transaction.views import NewTransactionView, MyTransactionView, EditTransactionView

urlpatterns = patterns('',
  url(r'^(?P<tableView>\d+)$', login_required(MyTransactionView.as_view())),
  url(r'^new/$', login_required(NewTransactionView.as_view())),
  url(r'^edit/(?P<pk>\d+)$', login_required(EditTransactionView.as_view())),
  url(r'^new/(?P<group_account_id>\d+)/$', login_required(NewTransactionView.as_view())),
)

urlpatterns += staticfiles_urlpatterns()
