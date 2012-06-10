from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from transaction.models import Transaction
from transaction.views import TransactionView, MyTransactionView, SelectGroupTransactionView

urlpatterns = patterns('',
    url(r'^$', login_required(MyTransactionView.as_view())),
    url(r'^all/$', login_required(TransactionView.as_view())),
    url(r'^new/$', login_required(SelectGroupTransactionView.as_view())),
    url(r'^new/(?P<groupId>\d+)/$', 'transaction.views.newTransaction'),
    url(r'^(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=Transaction,
            template_name='transaction/detail.html'))),
    
    #url(r'^buyer/(?P<buyerId>\d+)/$', BuyerDetailView.as_view()),
)

urlpatterns += staticfiles_urlpatterns()