import datetime
from django import forms
from groupaccountinvite.models import GroupAccountInvite
from userprofile.models import UserProfile
import logging

class NewInviteForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
#    groupAccountId = kwargs.pop('groupAccountId')
    
    logger = logging.getLogger(__name__)  
    logger.addHandler(logging.StreamHandler())
    
    userProfile = kwargs.pop('user')
    super(NewInviteForm, self).__init__(*args, **kwargs)
    
    self.fields['inviter'] = forms.ModelChoiceField(UserProfile.objects.filter(id=userProfile.id))
    self.fields['inviter'].initial = userProfile
    
    logger.warning(userProfile.groupAccounts)
        
    self.fields['invitee'] = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    
    self.fields['groupAccount'] = forms.ModelChoiceField(queryset=userProfile.groupAccounts, empty_label=None)

    self.fields['createdDateAndTime'] = forms.DateField(initial=datetime.date.today)
  
  class Meta:
    model = GroupAccountInvite
