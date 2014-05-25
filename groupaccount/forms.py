from django import forms
from groupaccount.models import GroupAccount

class NewGroupAccountForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(NewGroupAccountForm, self).__init__(*args, **kwargs)
    self.fields['name'] = forms.CharField(max_length=200, label='Group name')
    self.fields['number'] = forms.IntegerField(max_value=10000000000, min_value=0, label='Account number', help_text='Create your own group account number. Max 10 digits.')

  class Meta:
    model = GroupAccount
