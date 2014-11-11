from transactionreal.models import TransactionReal
from transaction.models import Modification
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

from django import forms

from datetime import datetime


class NewRealTransactionForm(forms.ModelForm):
  def __init__(self, groupAccountId, user, *args, **kwargs):
    super(NewRealTransactionForm, self).__init__(*args, **kwargs)
    
#     self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user), widget = forms.HiddenInput, empty_label=None, label='From')
    self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user=user), 
                                                   empty_label=None, label='From', widget=forms.HiddenInput())
    
    self.fields['sender'].initial = UserProfile.objects.get(user=user)    
    self.fields['receiver'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=groupAccountId), 
                                                     empty_label=None, label='To')
    
    self.fields['comment'] = forms.CharField(required=False)
    
    self.fields['amount'].label = '€'
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user).groupAccounts, widget=forms.Select(attrs={"onChange":'form.submit()'}), empty_label=None, label='Group')
    if GroupAccount.objects.filter(id=groupAccountId).count():
      self.fields['groupAccount'].initial = GroupAccount.objects.get(id=groupAccountId)
#     self.fields['groupAccount'].widget.attrs['readonly'] = True

    self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(), 
                                                                  required=False, 
                                                                  widget=forms.MultipleHiddenInput())
    self.fields['date'] = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now)
  
  class Meta:
    model = TransactionReal


class EditRealTransactionForm(forms.ModelForm):
  def __init__(self, transactionId, user, *args, **kwargs):
    super(EditRealTransactionForm, self).__init__(*args, **kwargs)
    
    transaction = TransactionReal.objects.get(id=transactionId)
    
    self.fields['amount'].label = '€'
    self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=transaction.groupAccount.id), 
                                                   empty_label=None, label='From', 
                                                   widget=forms.HiddenInput)
    
    self.fields['receiver'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(groupAccounts=transaction.groupAccount.id), 
                                                     empty_label=None, label='To')
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=GroupAccount.objects.filter(id=transaction.groupAccount.id), 
                                                         empty_label=None, 
                                                         label='Group')
    
    self.fields['groupAccount'].widget.attrs['readonly'] = True
    
    
    self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(), 
                                                                  required=False, 
                                                                  widget=forms.MultipleHiddenInput())
    
    self.fields['date'] = forms.DateTimeField(widget=forms.HiddenInput)
  
  class Meta:
    model = TransactionReal
    