import datetime
from django import forms
from transaction.models import Transaction
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class NewGroupAccountForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(NewGroupAccountForm, self).__init__(*args, **kwargs)

  class Meta:
    model = GroupAccount
