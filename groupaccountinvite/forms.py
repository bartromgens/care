import datetime
from django import forms
from groupaccountinvite.models import GroupAccountInvite
from userprofile.models import UserProfile

from datetime import datetime

import logging
logger = logging.getLogger(__name__)  

class NewInviteForm(forms.ModelForm):
  def __init__(self, user, *args, **kwargs):
#    groupAccountId = kwargs.pop('groupAccountId')
    
    userProfile = UserProfile.objects.get(user=user);
    super(NewInviteForm, self).__init__(*args, **kwargs)
    
    self.fields['inviter'] = forms.ModelChoiceField(UserProfile.objects.filter(id=userProfile.id), empty_label=None, label='User')
    self.fields['inviter'].initial = userProfile
    self.fields['inviter'].widget.attrs['readonly'] = True
    
    logger.debug(userProfile.groupAccounts)
        
    self.fields['invitee'] = forms.ModelChoiceField(queryset=UserProfile.objects.all(), label='Invites')
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=userProfile.groupAccounts, empty_label=None, label='To group')

    self.fields['isAccepted'] = forms.BooleanField(widget=forms.HiddenInput, required=False)
    self.fields['isDeclined'] = forms.BooleanField(widget=forms.HiddenInput, required=False)

    self.fields['createdDateAndTime'] = forms.DateTimeField(widget=forms.HiddenInput, initial=datetime.now, required=False)
  
  class Meta:
    model = GroupAccountInvite
