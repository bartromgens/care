from groupaccount.models import GroupAccount, GroupSetting 
from userprofile.models import NotificationInterval

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
        
        self.fields['settings'] = forms.ModelChoiceField( widget=forms.HiddenInput,
                                                          queryset=GroupSetting.objects.all(),
                                                          empty_label=None,
                                                          required=False )

    class Meta:
        model = GroupAccount


class EditGroupSettingForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(EditGroupSettingForm, self).__init__(*args, **kwargs)

        self.fields['notification_lower_limit'] = forms.IntegerField( min_value=0, 
                                                                      max_value=100000000000, 
                                                                      initial=0,
                                                                      label='Debt warning threshold (€)', 
                                                                      help_text='' )

        self.fields['notification_lower_limit_interval'] = forms.ModelChoiceField( queryset=NotificationInterval.objects.all(),
                                                                                   label='Email notification interval',
                                                                                   empty_label=None )


    class Meta:
        model = GroupSetting