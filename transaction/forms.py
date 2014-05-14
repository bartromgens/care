from datetime import datetime
from django import forms
from transaction.models import Transaction
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class NewTransactionForm(forms.ModelForm):
  def __init__(self, groupAccountId, user, *args, **kwargs):
    super(NewTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), label='Shared by')
    
    self.fields['buyer'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    self.fields['buyer'].initial = user
    self.fields['what'].label = 'What'
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user).groupAccounts, widget=forms.Select(attrs={"onChange":'form.submit()'}), empty_label=None, label='Group')
    self.fields['groupAccount'].initial = GroupAccount.objects.get(id=groupAccountId)
    self.fields['date'] = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.now)
  
  def setGroupAccount(self, groupAccount):
    self.fields['groupAccount'].initial = groupAccount
  
  class Meta:
    model = Transaction
