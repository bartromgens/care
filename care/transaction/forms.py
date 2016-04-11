from datetime import datetime
import logging

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

from care.transaction.models import Transaction
from care.transaction.models import TransactionReal
from care.transaction.models import Modification
from care.groupaccount.models import GroupAccount
from care.userprofile.models import UserProfile

logger = logging.getLogger(__name__)


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_shared_by_all'] = forms.BooleanField(label='Shared by all', required=False)
        self.fields['what'].label = 'What'
        self.fields['amount'].label = 'Cost (€)'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("consumers") and not cleaned_data.get("is_shared_by_all"):
            raise forms.ValidationError("Please select someone to share with.")
        return cleaned_data

    class Meta:
        model = Transaction
        fields = '__all__'


class NewTransactionForm(TransactionForm):
    def __init__(self, group_account_id, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['consumers'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=UserProfile.objects.filter(group_accounts=group_account_id),
            label='Shared by some',
            required=False
        )

        self.fields['buyer'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(group_accounts=group_account_id),
            empty_label=None
        )
        self.fields['buyer'].initial = UserProfile.objects.get(user=user)

        self.fields['group_account'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.get(user=user).group_accounts,
            widget=forms.Select(attrs={"onChange":'form.submit()'}),
            empty_label=None,
            label='Group'
        )
        if GroupAccount.objects.filter(id=group_account_id).count():
            self.fields['group_account'].initial = GroupAccount.objects.get(id=group_account_id)
            
        self.fields['date'] = forms.DateTimeField(
            widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
            initial=datetime.now
        )

        self.fields['modifications'] = forms.ModelMultipleChoiceField(
            queryset=Modification.objects.all(),
            required=False,
            widget=forms.MultipleHiddenInput()
        )

    def set_group_account(self, group_account):
        self.fields['group_account'].initial = group_account


class EditTransactionForm(TransactionForm):
    def __init__(self, transaction_id, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transaction = Transaction.objects.get(id=transaction_id)

        self.fields['consumers'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(),
            queryset=UserProfile.objects.filter(group_accounts=transaction.group_account),
            label='Shared by some',
            required=False
        )

        self.fields['buyer'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(group_accounts=transaction.group_account),
            empty_label=None
        )

        self.fields['group_account'] = forms.ModelChoiceField(
            queryset=GroupAccount.objects.filter(id=transaction.group_account.id),
            empty_label=None,
            label='Group'
        )

        self.fields['date'] = forms.DateTimeField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
        # self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(),
        #                                                               required=False,
        #                                                               widget=forms.MultipleHiddenInput())
        self.fields['group_account'].widget.attrs['readonly'] = True


class NewRealTransactionForm(forms.ModelForm):
    def __init__(self, group_account_id, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #  self.fields['sender'] = forms.ModelChoiceField(queryset=UserProfile.objects.get(user=user),
        #  widget = forms.HiddenInput, empty_label=None, label='From')
        self.fields['sender'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(user=user),
            empty_label=None,
            label='From',
            widget=forms.HiddenInput()
        )
        self.fields['sender'].initial = UserProfile.objects.get(user=user)
        self.fields['receiver'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(group_accounts=group_account_id),
            empty_label=None,
            label='To'
        )

        self.fields['comment'] = forms.CharField(required=False)
        self.fields['amount'].label = '€'

        self.fields['group_account'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.get(user=user).group_accounts,
            widget=forms.Select(attrs={"onChange":'form.submit()'}),
            empty_label=None,
            label='Group'
        )

        if GroupAccount.objects.filter(id=group_account_id).count():
            self.fields['group_account'].initial = GroupAccount.objects.get(id=group_account_id)
        # self.fields['modifications'] = forms.ModelMultipleChoiceField(queryset=Modification.objects.all(),
        #                                                               required=False,
        #                                                               widget=forms.MultipleHiddenInput())
        self.fields['date'] = forms.DateTimeField(
            widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
            initial=datetime.now
        )

    class Meta:
        model = TransactionReal
        fields = '__all__'


class EditRealTransactionForm(forms.ModelForm):
    def __init__(self, transaction_id, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

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