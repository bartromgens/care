from base.views import BaseView
from transaction.models import Transaction
from transaction.forms import NewTransactionForm, EditTransactionForm
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

    def get_number_of_buyer_transactions(self, buyerId):
        transactions = Transaction.objects.filter(buyer__id=buyerId)
        return len(transactions)

    def get_context_data(self, **kwargs):
        userProfile = UserProfile.objects.get(user=self.request.user)
        userProfile.get_show_table(self.kwargs['tableView'])
        context = super(MyTransactionView, self).get_context_data(**kwargs)
        transactionsAllSorted = Transaction.get_transactions_sorted_by_last_modified(userProfile.id)
        context['transactionsAll'] = transactionsAllSorted
        return context


class SelectGroupTransactionView(BaseView):
    template_name = "transaction/newselectgroup.html"
    context_object_name = "select transaction group"

    def get_context_data(self, **kwargs):
        context = super(SelectGroupTransactionView, self).get_context_data(**kwargs)

        userProfile = UserProfile.objects.get(user=self.request.user)
        groupaccounts = userProfile.groupAccounts.all
        context['groupaccounts'] = groupaccounts
        return context


class NewTransactionView(FormView, BaseView):
    template_name = 'transaction/new.html'
    form_class = NewTransactionForm
    success_url = '/transaction/new/success/'

    def get_active_menu(self):
        return 'shares'

    def get_groupaccount_id(self):
        if 'groupAccountId' in self.kwargs:
            return self.kwargs['groupAccountId']
        else:
            logger.debug(self.request.user.id)
            user = UserProfile.objects.get(user=self.request.user)
            if user.groupAccounts.count():
                return user.groupAccounts.all()[0].id
            else:
                return 0

    def get_form(self, form_class):
        return NewTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        super(NewTransactionView, self).form_valid(form)
        form.save()
        return HttpResponseRedirect( '/')

    def form_invalid(self, form):
        groupAccount = form.cleaned_data['groupAccount']
        if int(groupAccount.id) != int(self.get_groupaccount_id()):
            return HttpResponseRedirect( '/transactions/new/' + str(groupAccount.id))
        else:
            return super(NewTransactionView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(NewTransactionView, self).get_context_data(**kwargs)

        if (self.get_groupaccount_id()):
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
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        form.save()
        transaction.modifications.create(user=UserProfile.objects.get(user=self.request.user))
        return HttpResponseRedirect( '/transactions/0' )

    def get_context_data(self, **kwargs):
        context = super(EditTransactionView, self).get_context_data(**kwargs)
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        form = EditTransactionForm(self.kwargs['pk'], self.request.user, instance=transaction, **self.get_form_kwargs())
        context['form'] = form
        return context
