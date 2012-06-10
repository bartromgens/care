import datetime
from django import forms
from django.contrib.auth.models import User, Group
from transaction.models import Transaction

class NewTransactionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    groupId = kwargs.pop('groupId')
    user = kwargs.pop('user')
    super(NewTransactionForm, self).__init__(*args, **kwargs)
    
    self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.filter(groups=groupId))
    
    self.fields['buyer'] = forms.ModelChoiceField(queryset=User.objects.filter(groups=groupId), empty_label=None)
    self.fields['buyer'].initial = user
    
    self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(id=groupId), empty_label=None)

    self.fields['group'].widget.attrs['readonly'] = True

    self.fields['date'] = forms.DateField(initial=datetime.date.today)
  
  class Meta:
    model = Transaction
