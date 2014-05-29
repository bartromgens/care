from userprofile.forms import EditUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseView

from django.views.generic.edit import UpdateView


class EditUserProfileView(BaseView, UpdateView):
  model = UserProfile
  form_class = EditUserProfileForm
  template_name = 'userprofile/edit.html'
    
  def get_context_data(self, **kwargs):
    context = super(EditUserProfileView, self).get_context_data(**kwargs)
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