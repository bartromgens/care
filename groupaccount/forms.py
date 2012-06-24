from django import forms
from groupaccount.models import GroupAccount

class NewGroupAccountForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(NewGroupAccountForm, self).__init__(*args, **kwargs)

  class Meta:
    model = GroupAccount
