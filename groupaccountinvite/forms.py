import datetime
import logging
logger = logging.getLogger(__name__)

from django import forms

from groupaccountinvite.models import GroupAccountInvite
from userprofile.models import UserProfile


class NewInviteForm(forms.ModelForm):
    def __init__(self, user, user_profile_to_invite, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=user);
        super().__init__(*args, **kwargs)

        self.fields['inviter'] = forms.ModelChoiceField(UserProfile.objects.filter(id=user_profile.id), empty_label=None, label='You')
        self.fields['inviter'].initial = user_profile
        self.fields['inviter'].widget.attrs['readonly'] = True
        self.fields['invitee'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(id=user_profile_to_invite.id), empty_label=None, label='invite')
        self.fields['invitee'].initial = user_profile_to_invite
        self.fields['invitee'].widget.attrs['readonly'] = True
        self.fields['group_account'] = forms.ModelChoiceField(queryset=user_profile.group_accounts, empty_label=None, label='to group')
        self.fields['isAccepted'] = forms.BooleanField(widget=forms.HiddenInput, required=False)
        self.fields['isDeclined'] = forms.BooleanField(widget=forms.HiddenInput, required=False)
        self.fields['createdDateAndTime'] = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.datetime.now, required=False)

    class Meta:
        model = GroupAccountInvite
        fields = '__all__'

