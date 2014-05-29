from datetime import datetime
from django import forms
from transaction.models import Transaction
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

import logging
logger = logging.getLogger(__name__)
 

class NewTransactionForm(forms.ModelForm):
  def __init__(self, groupAccountId, user, *args, **kwargs):
    super(NewTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), label='Shared by')
    
    self.fields['buyer'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), empty_label=None)
    self.fields['buyer'].initial = user
    self.fields['what'].label = 'What'
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user).groupAccounts, widget=forms.Select(attrs={"onChange":'form.submit()'}), empty_label=None, label='Group')
    if GroupAccount.objects.filter(id=groupAccountId).count():
      self.fields['groupAccount'].initial = GroupAccount.objects.get(id=groupAccountId)
    self.fields['date'] = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.now)
  
  def setGroupAccount(self, groupAccount):
    self.fields['groupAccount'].initial = groupAccount
  
  class Meta:
    model = Transaction


class EditTransactionForm(forms.ModelForm):
  def __init__(self, transactionId, user, *args, **kwargs):
    super(EditTransactionForm, self).__init__(*args, **kwargs)
    
    transaction = Transaction.objects.get(id=transactionId)
    
    self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                                              queryset=UserProfile.objects.filter(groupAccounts=transaction.groupAccount), 
                                                              label='Shared by')
    
    self.fields['buyer'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=transaction.groupAccount), 
                                                  empty_label=None)
    self.fields['what'].label = 'What'
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=GroupAccount.objects.filter(id=transaction.groupAccount.id), 
                                                         empty_label=None, 
                                                         label='Group')
    
    self.fields['date'] = forms.DateTimeField(widget=forms.HiddenInput)
    
    self.fields['groupAccount'].widget.attrs['readonly'] = True
    
    logger.debug(transaction.consumers)
    
    self.fields['consumers'].initial = transaction.consumers.all()
#     self.fields['buyer'].initial = transaction.buyer
#     self.fields['what'].initial = transaction.what
#     self.fields['amount'].initial = transaction.amount
#     self.fields['groupAccount'].initial = GroupAccount.objects.get(id=transaction.groupAccount.id)
#     self.fields['date'].initial = transaction.date
  
  class Meta:
    model = Transaction
