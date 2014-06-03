from userprofile.forms import EditUserProfileForm, SearchUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseView

from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)


class EditUserProfileView(BaseView, FormView):
  template_name = 'userprofile/edit.html'
  form_class = EditUserProfileForm
  success_url = '/'  
    
  def get_form(self, form_class):
    pk = self.kwargs['pk']
    return EditUserProfileForm(self.request.user, instance=UserProfile.objects.get(pk=pk), **self.get_form_kwargs())   
# 
  def form_valid(self, form):
    logger.debug('EditUserProfileView')
    super(EditUserProfileView, self).form_valid(form)
    form.save()
    return HttpResponseRedirect( '/transactions/0' )
  
  def get_context_data(self, **kwargs):
    logger.debug('EditUserProfileView')
    context = super(EditUserProfileView, self).get_context_data(**kwargs)
    pk = self.kwargs['pk']
    form = EditUserProfileForm(self.request.user, instance=UserProfile.objects.get(pk=pk), **self.get_form_kwargs())
    context['form'] = form

    userProfile = UserProfile.objects.get(user=self.request.user)
    userProfileId = int(self.kwargs['pk'])
    # check whether user owns the UserProfile that is edited.
    if (userProfile.id == userProfileId):
      context['isAllowed'] = True;
    else:
      context.clear()    
      context['isAllowed'] = False;
    
    return context
  
  
class SuccessEditUserProfileView(BaseView):
  template_name = "userprofile/editsuccess.html"
  context_object_name = "select transaction group"
  
  def get_context_data(self, **kwargs):    
    context = super(SuccessEditUserProfileView, self).get_context_data(**kwargs)
    context['transactionssection'] = True
    
    return context


class SearchUserProfileView(BaseView, FormView):
  template_name = 'userprofile/search.html'
  form_class = SearchUserProfileForm
  success_url = '/userprofile/search'  
    
  def get_form(self, form_class):
    return SearchUserProfileForm(self.request.user, **self.get_form_kwargs())   
# 
  def form_valid(self, form):
    username = form.cleaned_data['username']
    users = User.objects.filter(username__icontains=username)
    userProfiles = UserProfile.objects.filter(Q(user=users) | Q(displayname__icontains=username) | Q(firstname__icontains=username) | Q(lastname__icontains=username))
    for user in userProfiles:
      logger.debug(str(user.displayname))
      
    context = super(SearchUserProfileView, self).get_context_data()  
    form = SearchUserProfileForm(self.request.user, **self.get_form_kwargs())
    context['form'] = form
    context['hasSearched'] = True
    context['searchresults'] = userProfiles
    return self.render_to_response(context)
  
  def get_context_data(self, **kwargs):
    context = super(SearchUserProfileView, self).get_context_data(**kwargs)
    form = SearchUserProfileForm(self.request.user, **self.get_form_kwargs())
    context['form'] = form
    
    return context
  