from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from care.transaction.models import Transaction
from care.transaction.views import NewTransactionView, MyTransactionView, EditTransactionView
from care.transaction.views import NewRecurringTransactionView, MyRecurringTransactionView, EditRecurringTransactionView
from care.transaction.views import NewRealTransactionView, MyRealTransactionView, EditRealTransactionView


urlpatterns = [
    url(r'^share/(?P<tableView>\d+)/$', login_required(MyTransactionView.as_view())),
    url(r'^share/new/$', login_required(NewTransactionView.as_view())),
    url(r'^share/edit/(?P<pk>\d+)/$', login_required(EditTransactionView.as_view())),
    url(r'^share/new/(?P<group_account_id>\d+)/$', login_required(NewTransactionView.as_view())),

    url(r'^recurring/(?P<tableView>\d+)/$',
        login_required(MyRecurringTransactionView.as_view())),
    url(r'^recurring/new/$',
        login_required(NewRecurringTransactionView.as_view())),
    url(r'^recurring/edit/(?P<pk>\d+)/$',
        login_required(EditRecurringTransactionView.as_view())),
    url(r'^recurring/new/(?P<group_account_id>\d+)/$',
        login_required(NewRecurringTransactionView.as_view())),

    url(r'^real/(?P<tableView>\d+)/$', login_required(MyRealTransactionView.as_view())),
    url(r'^real/new/$', login_required(NewRealTransactionView.as_view())),
    url(r'^real/new/(?P<group_account_id>\d+)/$', login_required(NewRealTransactionView.as_view())),
    url(r'^real/edit/(?P<pk>\d+)$', login_required(EditRealTransactionView.as_view())),
    url(r'^real/(?P<pk>\d+)/$', login_required(DetailView.as_view(model=Transaction, template_name='transaction/detail.html'))),
]

urlpatterns += staticfiles_urlpatterns()
