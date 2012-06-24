from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class LoginForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)
  
class UserCreateForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super(UserCreateForm, self).__init__(*args, **kwargs)
    
  email = forms.EmailField(required=True)
  
  class Meta:
    model = User 
    fields = ("username", "email", "password1", "password2")
    
#class GroupCreateForm(forms.ModelForm):
#  def __init__(self, *args, **kwargs):
#    super(GroupCreateForm, self).__init__(*args, **kwargs)
#  
#  class Meta:
#    model = Group
#    fields = ('name',)