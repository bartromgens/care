import datetime
from django import forms
from django.contrib.auth.models import User, Group
from transactionreal.models import TransactionReal

class NewRealTransactionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    groupId = kwargs.pop('groupId')
    user = kwargs.pop('user')
    super(NewRealTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['sender'] = forms.ModelChoiceField(queryset=User.objects.filter(groups=groupId), empty_label=None)
    self.fields['sender'].initial = user    
    self.fields['receiver'] = forms.ModelChoiceField(queryset=User.objects.filter(groups=groupId), empty_label=None)
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=Group.objects.filter(id=groupId), empty_label=None)

    self.fields['groupAccount'].widget.attrs['readonly'] = True

    self.fields['date'] = forms.DateField(initial=datetime.date.today)
  
  class Meta:
    model = TransactionReal
