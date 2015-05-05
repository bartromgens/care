import datetime
from django import forms
from groupaccountinvite.models import GroupAccountInvite
from userprofile.models import UserProfile

import logging
logger = logging.getLogger(__name__)

class NewInviteForm(forms.ModelForm):
    def __init__(self, user, userProfileToInvite, *args, **kwargs):
#    groupAccountId = kwargs.pop('groupAccountId')

        userProfile = UserProfile.objects.get(user=user);
        super(NewInviteForm, self).__init__(*args, **kwargs)

        self.fields['inviter'] = forms.ModelChoiceField(UserProfile.objects.filter(id=userProfile.id), empty_label=None, label='You')
        self.fields['inviter'].initial = userProfile
        self.fields['inviter'].widget.attrs['readonly'] = True

        logger.debug(userProfile.groupAccounts)

        self.fields['invitee'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(id=userProfileToInvite.id), empty_label=None, label='invite')
        self.fields['invitee'].initial = userProfileToInvite
        self.fields['invitee'].widget.attrs['readonly'] = True

        self.fields['groupAccount'] = forms.ModelChoiceField(queryset=userProfile.groupAccounts, empty_label=None, label='to group')

        self.fields['isAccepted'] = forms.BooleanField(widget=forms.HiddenInput, required=False)
        self.fields['isDeclined'] = forms.BooleanField(widget=forms.HiddenInput, required=False)

        self.fields['createdDateAndTime'] = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.datetime.now, required=False)

    class Meta:
        model = GroupAccountInvite
        fields = '__all__'

