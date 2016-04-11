from random import randint

from django import forms

from care.groupaccount.models import GroupAccount, GroupSetting
from care.userprofile.models import NotificationInterval


class NewGroupAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(max_length=200, label='Group name')
        self.fields['number'] = forms.IntegerField(widget=forms.HiddenInput, min_value=0, max_value=100000000000, label='Account number', help_text='Create your own group account number. Max 10 digits.')

        random_num = randint(9999999999,100000000000)
        group_account = GroupAccount.objects.filter(number=random_num)
        while group_account:
            random_num = randint(9999999999,100000000000)
            group_account = GroupAccount.objects.filter(number=random_num)

        self.fields['number'].initial = random_num
        self.fields['settings'] = forms.ModelChoiceField( widget=forms.HiddenInput,
                                                          queryset=GroupSetting.objects.all(),
                                                          empty_label=None,
                                                          required=False )

    class Meta:
        model = GroupAccount
        fields = '__all__'


class EditGroupSettingForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['notification_lower_limit'] = forms.IntegerField( min_value=-1000, 
                                                                      max_value=0, 
                                                                      initial=-100,
                                                                      label='Balance reminder threshold (€)', 
                                                                      help_text="A reminder is sent when someone\'s balance is lower than this value." )

        self.fields['notification_lower_limit_interval'] = forms.ModelChoiceField( queryset=NotificationInterval.objects.all(),
                                                                                   label='Email notification interval',
                                                                                   empty_label=None,
                                                                                   help_text="The interval of the balance reminder email." )

    class Meta:
        model = GroupSetting
        fields = '__all__'
