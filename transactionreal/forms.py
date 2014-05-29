from datetime import datetime
from django import forms
from transactionreal.models import TransactionReal
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class NewRealTransactionForm(forms.ModelForm):
  def __init__(self, groupAccountId, user, *args, **kwargs):
    super(NewRealTransactionForm, self).__init__(*args, **kwargs)
    
#     self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user), widget = forms.HiddenInput, empty_label=None, label='From')
    self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user=user), empty_label=None, label='From', widget=forms.HiddenInput)
    self.fields['sender'].initial = UserProfile.objects.get(user=user).id    
    self.fields['receiver'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None, label='To')
    
    self.fields['comment'] = forms.CharField(required=False)
    
    self.fields['amount'].label = '€'
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user).groupAccounts, widget=forms.Select(attrs={"onChange":'form.submit()'}), empty_label=None, label='Group')
    if GroupAccount.objects.filter(id=groupAccountId).count():
      self.fields['groupAccount'].initial = GroupAccount.objects.get(id=groupAccountId)
#     self.fields['groupAccount'].widget.attrs['readonly'] = True

    self.fields['date'] = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.now)
  
  class Meta:
    model = TransactionReal
