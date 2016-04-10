from datetime import datetime
from django import forms
from transaction.models import Transaction
from transaction.models import TransactionReal
from transaction.models import Modification
from groupaccount.models import GroupAccount
from userprofile.models import UserProfile

from bootstrap3_datetime.widgets import DateTimePicker

import logging
logger = logging.getLogger(__name__)


class NewTransactionForm(forms.ModelForm):
    ## TODO BR: remove duplicate code with EditTransactionForm
    def __init__(self, group_account_id, user, *args, **kwargs):
        super(NewTransactionForm, self).__init__(*args, **kwargs)

        self.fields['is_shared_by_all'] = forms.BooleanField(label='Shared by all', required=False)
        self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), 
                                                                  queryset=UserProfile.objects.filter(group_accounts=group_account_id),
                                                                  label='Shared by some', required=False)

        self.fields['buyer'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(group_accounts=group_account_id),
                                                      empty_label=None)

        self.fields['buyer'].initial = UserProfile.objects.get(user=user)
        self.fields['what'].label = 'What'
        self.fields['amount'].label = 'Cost (€)'
        self.fields['group_account'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user).group_accounts,
                                                              widget=forms.Select(attrs={"onChange":'form.submit()'}),
                                                              empty_label=None,
                                                              label='Group')
        if GroupAccount.objects.filter(id=group_account_id).count():
            self.fields['group_account'].initial = GroupAccount.objects.get(id=group_account_id)
            
        self.fields['date'] = forms.DateTimeField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}), 
                                                  initial=datetime.now)

        self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(), 
                                                                      required=False, 
                                                                      widget=forms.MultipleHiddenInput())

    def set_group_account(self, group_account):
        self.fields['group_account'].initial = group_account

    def clean(self):
        cleaned_data = super(NewTransactionForm, self).clean()
        if not cleaned_data.get("consumers") and not cleaned_data.get("is_shared_by_all"):
            raise forms.ValidationError("Please select someone to share with.")
        return cleaned_data

    class Meta:
        model = Transaction
        fields = '__all__'


class EditTransactionForm(forms.ModelForm):
    def __init__(self, transaction_id, user, *args, **kwargs):
        super(EditTransactionForm, self).__init__(*args, **kwargs)

        transaction = Transaction.objects.get(id=transaction_id)

        self.fields['is_shared_by_all'] = forms.BooleanField(label='Shared by all', required=False)
        self.fields['consumers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                                  queryset=UserProfile.objects.filter(group_accounts=transaction.group_account),
                                                                  label='Shared by some', required=False)
        self.fields['buyer'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(group_accounts=transaction.group_account),
                                                      empty_label=None)
        self.fields['what'].label = 'What'
        self.fields['amount'].label = 'Cost (€)'
        self.fields['group_account'] = forms.ModelChoiceField(queryset=GroupAccount.objects.filter(id=transaction.group_account.id),
                                                             empty_label=None,
                                                             label='Group')
        self.fields['date'] = forms.DateTimeField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
        # self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(),
        #                                                               required=False,
        #                                                               widget=forms.MultipleHiddenInput())
        self.fields['group_account'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(EditTransactionForm, self).clean()
        if not cleaned_data.get("consumers") and not cleaned_data.get("is_shared_by_all"):
            raise forms.ValidationError("Please select someone to share with.")
        return cleaned_data

    class Meta:
        model = Transaction
        fields = '__all__'


class NewRealTransactionForm(forms.ModelForm):
    def __init__(self, group_account_id, user, *args, **kwargs):
        super(NewRealTransactionForm, self).__init__(*args, **kwargs)

        #  self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user),
        #  widget = forms.HiddenInput, empty_label=None, label='From')
        self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user=user),
                                                       empty_label=None, label='From', widget=forms.HiddenInput())
        self.fields['sender'].initial = UserProfile.objects.get(user=user)
        self.fields['receiver'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(group_accounts=group_account_id),
                                                         empty_label=None, label='To')
        self.fields['comment'] = forms.CharField(required=False)
        self.fields['amount'].label = '€'
        self.fields['group_account'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user).group_accounts, widget=forms.Select(attrs={"onChange":'form.submit()'}), empty_label=None, label='Group')
        if GroupAccount.objects.filter(id=group_account_id).count():
            self.fields['group_account'].initial = GroupAccount.objects.get(id=group_account_id)
        # self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(),
        #                                                               required=False,
        #                                                               widget=forms.MultipleHiddenInput())
        self.fields['date'] = forms.DateTimeField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
                                                  initial=datetime.now)

    class Meta:
        model = TransactionReal
        fields = '__all__'


class EditRealTransactionForm(forms.ModelForm):
    def __init__(self, transaction_id, user, *args, **kwargs):
        super(EditRealTransactionForm, self).__init__(*args, **kwargs)

        transaction = TransactionReal.objects.get(id=transaction_id)

        self.fields['amount'].label = '€'
        self.fields['sender'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(group_accounts=transaction.group_account.id),
            empty_label=None, label='From',
            widget=forms.HiddenInput)

        self.fields['receiver'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(group_accounts=transaction.group_account.id),
            empty_label=None, label='To')

        self.fields['group_account'] = forms.ModelChoiceField(
            queryset=GroupAccount.objects.filter(id=transaction.group_account.id),
            empty_label=None,
            label='Group')

        self.fields['group_account'].widget.attrs['readonly'] = True
        self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(),
                                                                      required=False,
                                                                      widget=forms.MultipleHiddenInput())

        self.fields['date'] = forms.DateTimeField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))

    class Meta:
        model = TransactionReal
        fields = '__all__'