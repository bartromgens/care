from groupaccount.models import GroupAccount

from django import forms

from random import randint

class NewGroupAccountForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(NewGroupAccountForm, self).__init__(*args, **kwargs)
    self.fields['name'] = forms.CharField(max_length=200, label='Group name')
    self.fields['number'] = forms.IntegerField(widget=forms.HiddenInput, min_value=0, max_value=100000000000, label='Account number', help_text='Create your own group account number. Max 10 digits.')
    
    randomNumber = randint(9999999999,100000000000)
    groupAccount = GroupAccount.objects.filter(number=randomNumber)
    while groupAccount:
      randomNumber = randint(9999999999,100000000000)
      groupAccount = GroupAccount.objects.filter(number=randomNumber)
      
    self.fields['number'].initial = randomNumber
    
  class Meta:
    model = GroupAccount
