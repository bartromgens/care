from django.views.generic.edit import UpdateView
from userprofile.forms import EditUserProfileForm
from userprofile.models import UserProfile
from base.views import BaseView

class EditUserProfileView(UpdateView):
  model = UserProfile
  form_class = EditUserProfileForm
  template_name = 'userprofile/edit.html'
    
  def get_context_data(self, **kwargs):
    context = super(EditUserProfileView, self).get_context_data(**kwargs)
    userProfile = UserProfile.objects.get(user=self.request.user)
    print type(userProfile.id) 
    print type(self.kwargs['pk'])
    
    if (userProfile.id == int(self.kwargs['pk'])):
      print 'correct user'
    else:
      print 'wrong user'    
    
    return context