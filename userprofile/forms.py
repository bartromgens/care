from django import forms
from django.contrib.auth.models import User

from userprofile.models import UserProfile, NotificationInterval


class EditUserProfileForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)

        userProfile = UserProfile.objects.get(user=user)
        self.fields['user'] = forms.ModelChoiceField(widget=forms.HiddenInput,
                                                     queryset=User.objects.filter(id=user.id),
                                                     empty_label=None)
        self.fields['displayname'] = forms.CharField(max_length=15, label='Display name *')
        self.fields['firstname'] = forms.CharField(max_length=100, label='First name', required=False)
        self.fields['lastname'] = forms.CharField(max_length=100, label='Last name', required=False)
        self.fields['showTableView'] = forms.BooleanField(widget=forms.HiddenInput, required=False)
        self.fields['group_accounts'] = forms.ModelMultipleChoiceField(widget=forms.MultipleHiddenInput,
                                                                      queryset=userProfile.group_accounts.all(),
                                                                      label='Groups',
                                                                      required=False)
        self.fields['historyEmailInterval'] = forms.ModelChoiceField(queryset=NotificationInterval.objects.all(),
                                                                     label='Transaction history email',
                                                                     empty_label=None)

    class Meta:
        model = UserProfile
        fields = '__all__'


class SearchUserProfileForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(SearchUserProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(min_length=3, max_length=100, label='Name or part of name', required=True)
