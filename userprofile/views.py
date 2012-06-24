from django.views.generic.edit import UpdateView
from userprofile.forms import EditUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseUpdateView

class EditUserProfileView(BaseUpdateView):
  model = UserProfile
  form_class = EditUserProfileForm
  template_name = 'userprofile/edit.html'
    
  def get_context_data(self, **kwargs):
    context = super(EditUserProfileView, self).get_context_data(**kwargs)
    userProfile = UserProfile.objects.get(user=self.request.user)
    print type(userProfile.id) 
    print type(self.kwargs['pk'])
    
    # check whether user owns the UserProfile that is edited.
    if (userProfile.id == int(self.kwargs['pk'])):
      context['isAllowed'] = True;
    else:
      context.clear()    
      context['isAllowed'] = False;
    
    return context