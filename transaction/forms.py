from datetime import datetime
from django import forms
from transaction.models import Transaction
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

class NewTransactionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    groupAccountId = kwargs.pop('groupAccountId')
    user = kwargs.pop('user')
    super(NewTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=UserProfile.objects.filter(groupAccounts=groupAccountId))
    
    self.fields['buyer'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    self.fields['buyer'].initial = user
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=GroupAccount.objects.filter(id=groupAccountId), empty_label=None)

    self.fields['groupAccount'].widget.attrs['readonly'] = True

    self.fields['date'] = forms.DateField(initial=datetime.now())
  
  class Meta:
    model = Transaction
