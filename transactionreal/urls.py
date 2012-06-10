from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView
from transaction.models import Transaction
from transactionreal.views import SelectGroupRealTransactionView

urlpatterns = patterns('',
    url(r'^new/$', login_required(SelectGroupRealTransactionView.as_view())),
    url(r'^new/(?P<groupId>\d+)/$', 'transactionreal.views.newRealTransaction'),
    url(r'^(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=Transaction,
            template_name='transaction/detail.html'))),
    
    #url(r'^buyer/(?P<buyerId>\d+)/$', BuyerDetailView.as_view()),
)

urlpatterns += staticfiles_urlpatterns()