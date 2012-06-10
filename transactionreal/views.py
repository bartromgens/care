# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

from base.views import BaseView
from transactionreal.forms import NewRealTransactionForm
from userprofile.models import UserProfile

class SelectGroupRealTransactionView(BaseView):
  template_name = "transactionreal/newselectgroup.html"
  context_object_name = "select transaction group"
  
  def get_context_data(self, **kwargs):    
    context = super(SelectGroupRealTransactionView, self).get_context_data(**kwargs)
    
    userProfile = UserProfile.objects.get(user=self.request.user)
    groupaccounts = userProfile.groupAccounts.all
    context['groupaccounts'] = groupaccounts
    context['transactionssection'] = True
    
    return context

def newRealTransaction(request, groupAccountId):
  def errorHandle(error):
    kwargs = {'user' : request.user, 'groupAccountId' : groupAccountId}
    form = NewRealTransactionForm(**kwargs)
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
      context['transactionssection'] = True
    return render_to_response('transactionreal/new.html', context)
          
  if request.method == 'POST': # If the form has been submitted...
    kwargs = {'user' : request.user, 'groupAccountId' : groupAccountId}
    form = NewRealTransactionForm(request.POST, **kwargs) # A form bound to the POST data
    
    if form.is_valid(): # All validation rules pass
      form.save()
      context = RequestContext(request)

      if request.user.is_authenticated():
        context['user'] = request.user
        context['isLoggedin'] = True
        context['transactionssection'] = True

      return render_to_response('transactionreal/newsuccess.html', context)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  
  else:
    kwargs = {'user' : request.user, 'groupAccountId' : groupAccountId}
    form = NewRealTransactionForm(**kwargs) # An unbound form
    context = RequestContext(request)
    context['form'] = form
    context['transactionssection'] = True
    
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
    return render_to_response('transactionreal/new.html', context)