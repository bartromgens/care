import datetime
from django import forms
from transactionreal.models import TransactionReal
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class NewRealTransactionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    groupAccountId = kwargs.pop('groupAccountId')
    user = kwargs.pop('user')
    super(NewRealTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    self.fields['sender'].initial = user    
    self.fields['receiver'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=GroupAccount.objects.filter(id=groupAccountId), empty_label=None)

    self.fields['groupAccount'].widget.attrs['readonly'] = True

    self.fields['date'] = forms.DateField(initial=datetime.date.today)
  
  class Meta:
    model = TransactionReal
