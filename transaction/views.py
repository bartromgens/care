from base.views import BaseView
from transaction.models import Transaction
from transaction.models import TransactionReal
from transaction.models import Modification
from transaction.forms import NewTransactionForm, EditTransactionForm
from transaction.forms import NewRealTransactionForm, EditRealTransactionForm
from userprofile.models import UserProfile

from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)


class MyTransactionView(BaseView):
    template_name = "transaction/mytransactions.html"
    context_object_name = "my transactions"

    def get_active_menu(self):
        return 'shares'

    @staticmethod
    def get_number_of_buyer_transactions(buyer_id):
        transactions = Transaction.objects.filter(buyer__id=buyer_id)
        return len(transactions)

    def get_context_data(self, **kwargs):
        userprofile = UserProfile.objects.get(user=self.request.user)
        userprofile.get_show_table(self.kwargs['tableView'])
        context = super(MyTransactionView, self).get_context_data(**kwargs)
        transactions_all_sorted = Transaction.get_transactions_sorted_by_last_modified(userprofile.id)
        context['transactionsAll'] = transactions_all_sorted
        return context


class SelectGroupTransactionView(BaseView):
    template_name = "transaction/newselectgroup.html"
    context_object_name = "select transaction group"

    def get_context_data(self, **kwargs):
        context = super(SelectGroupTransactionView, self).get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        groupaccounts = user_profile.group_accounts.all
        context['groupaccounts'] = groupaccounts
        return context


class NewTransactionView(FormView, BaseView):
    template_name = 'transaction/new.html'
    form_class = NewTransactionForm
    success_url = '/transaction/new/success/'

    def get_active_menu(self):
        return 'shares'

    def get_groupaccount_id(self):
        if 'group_account_id' in self.kwargs:
            return self.kwargs['group_account_id']
        else:
            logger.debug(self.request.user.id)
            user = UserProfile.objects.get(user=self.request.user)
            if user.group_accounts.count():
                return user.group_accounts.all()[0].id
            else:
                return 0

    def get_form(self, form_class):
        return NewTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        super(NewTransactionView, self).form_valid(form)
        form.save()
        transaction = Transaction.objects.get(pk=form.instance.id)
        Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction=transaction)
        return HttpResponseRedirect('/transactions/share/0')

    def form_invalid(self, form):
        group_account = form.cleaned_data['group_account']
        if int(group_account.id) != int(self.get_groupaccount_id()):
            return HttpResponseRedirect( '/transactions/new/' + str(group_account.id))
        else:
            return super(NewTransactionView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(NewTransactionView, self).get_context_data(**kwargs)

        if self.get_groupaccount_id():
            form = NewTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())
            context['form'] = form
            context['nogroup'] = False
        else:
            context['nogroup'] = True
        return context


class EditTransactionView(FormView, BaseView):
    template_name = 'transaction/edit.html'
    form_class = EditTransactionForm
    success_url = '/transactions/0'

    def get_active_menu(self):
        return 'shares'

    def get_form(self, form_class):
        pk = self.kwargs['pk']
        transaction = Transaction.objects.get(pk=pk)
        return EditTransactionForm(pk, self.request.user, instance=transaction, **self.get_form_kwargs())

    def form_valid(self, form):
        super(EditTransactionView, self).form_valid(form)
        form.save()
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction=transaction)
        return HttpResponseRedirect('/transactions/share/0')

    def get_context_data(self, **kwargs):
        context = super(EditTransactionView, self).get_context_data(**kwargs)
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        form = EditTransactionForm(self.kwargs['pk'], self.request.user, instance=transaction, **self.get_form_kwargs())
        context['form'] = form
        return context


class MyRealTransactionView(BaseView):
    template_name = "transactionreal/mytransactionsreal.html"
    context_object_name = "my real transactions"

    def get_active_menu(self):
        return 'transactions'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profile.get_show_table(self.kwargs['tableView'])
        context = super(MyRealTransactionView, self).get_context_data(**kwargs)
        transactions_real_all_sorted = TransactionReal.get_transactions_real_sorted_by_last_modified(user_profile.id)
        context['transactionsRealAll'] = transactions_real_all_sorted
        return context


class SelectGroupRealTransactionView(BaseView):
    template_name = "transactionreal/newselectgroup.html"
    context_object_name = "select transaction group"

    def get_context_data(self, **kwargs):
        context = super(SelectGroupRealTransactionView, self).get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        groupaccounts = user_profile.group_accounts.all
        context['groupaccounts'] = groupaccounts
        context['transactionssection'] = True
        return context


class NewRealTransactionView(FormView, BaseView):
    template_name = 'transactionreal/new.html'
    form_class = NewRealTransactionForm
    success_url = '/transactionreal/new/success/'

    def get_active_menu(self):
        return 'transactions'

    def get_groupaccount_id(self):
        if 'group_account_id' in self.kwargs:
            return self.kwargs['group_account_id']
        else:
            logger.debug(self.request.user.id)
            user = UserProfile.objects.get(user=self.request.user)
            if user.group_accounts.count():
                return user.group_accounts.all()[0].id
            else:
                return 0

    def get_form(self, form_class):
        logger.debug('get_form()')
        return NewRealTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        logger.debug('form_valid()')
        super(NewRealTransactionView, self).form_valid(form)
        form.save()
        transaction = TransactionReal.objects.get(pk=form.instance.id)
        Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction_real=transaction)
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        logger.debug('form_invalid()')
        group_account = form.cleaned_data['group_account']
        super(NewRealTransactionView, self).form_invalid(form)
        return HttpResponseRedirect( '/transactionsreal/new/' + str(group_account.id))

    def get_context_data(self, **kwargs):
        logger.debug('NewRealTransactionView::get_context_data() - group_account_id: ' + str(self.get_groupaccount_id()))
        context = super(NewRealTransactionView, self).get_context_data(**kwargs)

        if self.get_groupaccount_id():
            form = NewRealTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())
            context['form'] = form
            context['nogroup'] = False
        else:
            context['nogroup'] = True
        return context


class EditRealTransactionView(FormView, BaseView):
    template_name = 'transactionreal/edit.html'
    form_class = EditRealTransactionForm
    success_url = '/transactionsreal/0'

    def get_active_menu(self):
        return 'transactions'

    def get_form(self, form_class):
        pk = self.kwargs['pk']
        transaction = TransactionReal.objects.get(pk=pk)
        return EditRealTransactionForm(pk, self.request.user, instance=transaction, **self.get_form_kwargs())

    def form_valid(self, form):
        logger.debug('EditRealTransactionView::form_valid()')
        super(EditRealTransactionView, self).form_valid(form)
        transactionreal = TransactionReal.objects.get(pk=self.kwargs['pk'])
        if self.request.user == transactionreal.sender.user or self.request.user == transactionreal.receiver.user:
            form.save()
            Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction_real=transactionreal)
        return HttpResponseRedirect('/transactions/real/0')


    def get_context_data(self, **kwargs):
        context = super(EditRealTransactionView, self).get_context_data(**kwargs)
        transaction = TransactionReal.objects.get(pk=self.kwargs['pk'])

        if self.request.user == transaction.sender.user or self.request.user == transaction.receiver.user:
            form = EditRealTransactionForm(self.kwargs['pk'], self.request.user,
                                           instance=transaction, **self.get_form_kwargs())
            context['form'] = form

        return context
