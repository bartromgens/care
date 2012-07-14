from datetime import datetime
from django import forms
from transactionreal.models import TransactionReal
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class NewRealTransactionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    groupAccountId = kwargs.pop('groupAccountId')
    userProfile = kwargs.pop('userProfile')
    super(NewRealTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    self.fields['sender'].initial = userProfile    
    self.fields['receiver'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    
    self.fields['comment'] = forms.CharField(required=False)
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=GroupAccount.objects.filter(id=groupAccountId), empty_label=None)

    self.fields['groupAccount'].widget.attrs['readonly'] = True

    self.fields['date'] = forms.DateField(initial=datetime.now())
  
  class Meta:
    model = TransactionReal
