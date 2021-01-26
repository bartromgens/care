import logging

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from care.base.views import BaseView
from care.transaction.models import Transaction
from care.transaction.models import TransactionRecurring
from care.transaction.models import TransactionReal
from care.transaction.models import Modification
from care.transaction.forms import NewTransactionForm, EditTransactionForm
from care.transaction.forms \
    import NewRecurringTransactionForm, EditRecurringTransactionForm
from care.transaction.forms import NewRealTransactionForm, EditRealTransactionForm
from care.userprofile.models import UserProfile

logger = logging.getLogger(__name__)


class MyTransactionView(BaseView):
    template_name = "transaction/share/mytransactions.html"
    context_object_name = "my transactions"

    def get_active_menu(self):
        return 'shares'

    def get_context_data(self, **kwargs):
        userprofile = UserProfile.objects.get(user=self.request.user)
        userprofile.get_show_table(self.kwargs['tableView'])
        context = super().get_context_data(**kwargs)
        transactions_all_sorted = Transaction.get_transactions_sorted_by_last_modified(userprofile.id)
        paginator = Paginator(transactions_all_sorted, 25)

        page = self.request.GET.get('page')
        try:
            transactions_all_sorted = paginator.page(page)
        except PageNotAnInteger:
            transactions_all_sorted = paginator.page(1)
        except EmptyPage:
            transactions_all_sorted = paginator.page(paginator.num_pages)
        context['transactions_all'] = transactions_all_sorted
        return context


class SelectGroupTransactionView(BaseView):
    template_name = "transaction/share/newselectgroup.html"
    context_object_name = "select transaction group"

    def get_context_data(self, **kwargs):
        context = super(SelectGroupTransactionView, self).get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        groupaccounts = user_profile.group_accounts.all
        context['groupaccounts'] = groupaccounts
        return context


class NewTransactionView(FormView, BaseView):
    template_name = 'transaction/share/new.html'
    form_class = NewTransactionForm
    success_url = '/transactions/share/new/success/'

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

    def get_form(self, form_class=NewTransactionForm):
        return NewTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        super().form_valid(form)
        if form.cleaned_data['is_shared_by_all']:
            form.cleaned_data['consumers'] = UserProfile.objects.filter(group_accounts=form.cleaned_data['group_account'])
        form.save()
        transaction = Transaction.objects.get(pk=form.instance.id)
        Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction=transaction)
        return HttpResponseRedirect('/transactions/share/0')

    def form_invalid(self, form):
        # Updates the Buyer dropdown in case the Group has changed
        group_account = form.cleaned_data['group_account']
        if int(group_account.id) != int(self.get_groupaccount_id()):
            return HttpResponseRedirect('/transactions/share/new/' + str(group_account.id))
        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_groupaccount_id():
            context['nogroup'] = False
        else:
            context['nogroup'] = True
        return context


class EditTransactionView(FormView, BaseView):
    template_name = 'transaction/share/edit.html'
    form_class = EditTransactionForm
    success_url = '/transactions/share/0'

    def get_active_menu(self):
        return 'shares'

    def get_form(self, form_class=EditTransactionForm):
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        return EditTransactionForm(instance=transaction, **self.get_form_kwargs())

    def form_valid(self, form):
        super().form_valid(form)
        if form.cleaned_data['is_shared_by_all']:
            form.cleaned_data['consumers'] = UserProfile.objects.filter(group_accounts=form.cleaned_data['group_account'])
        form.save()
        transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        modif = Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction=transaction)
        transaction.last_modified = modif.date
        transaction.save()
        return HttpResponseRedirect('/transactions/share/0')


class MyRecurringTransactionView(BaseView):
    template_name = "transaction/recurring/mytransactions.html"
    context_object_name = "my recurring transactions"

    def get_active_menu(self):
        return 'recurring'

    def get_context_data(self, **kwargs):
        userprofile = UserProfile.objects.get(user=self.request.user)
        userprofile.get_show_table(self.kwargs['tableView'])
        context = super().get_context_data(**kwargs)
        transactions_all_sorted = \
            TransactionRecurring.get_transactions_sorted_by_last_modified(userprofile.id)
        paginator = Paginator(transactions_all_sorted, 25)

        page = self.request.GET.get('page')
        try:
            transactions_all_sorted = paginator.page(page)
        except PageNotAnInteger:
            transactions_all_sorted = paginator.page(1)
        except EmptyPage:
            transactions_all_sorted = paginator.page(paginator.num_pages)
        context['transactions_all'] = transactions_all_sorted
        return context


class SelectGroupRecurringTransactionView(BaseView):
    template_name = "transaction/recurring/newselectgroup.html"
    context_object_name = "select recurring transaction group"

    def get_context_data(self, **kwargs):
        context = super(SelectGroupRecurringTransactionView, self) \
            .get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        groupaccounts = user_profile.group_accounts.all
        context['groupaccounts'] = groupaccounts
        return context


class NewRecurringTransactionView(FormView, BaseView):
    template_name = 'transaction/recurring/new.html'
    form_class = NewRecurringTransactionForm
    success_url = '/transactions/recurring/new/success/'

    def get_active_menu(self):
        return 'recurring'

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

    def get_form(self, form_class=NewRecurringTransactionForm):
        return NewRecurringTransactionForm(self.get_groupaccount_id(),
                                           self.request.user,
                                           **self.get_form_kwargs())

    def form_valid(self, form):
        super().form_valid(form)
        if form.cleaned_data['is_shared_by_all']:
            form.cleaned_data['consumers'] = UserProfile.objects.filter(
                group_accounts=form.cleaned_data['group_account'])
        form.save()
        transaction = TransactionRecurring.objects.get(pk=form.instance.id)
        Modification.objects.create(
            user=UserProfile.objects.get(user=self.request.user),
            transaction_recurring=transaction)
        return HttpResponseRedirect('/transactions/recurring/0')

    def form_invalid(self, form):
        # Updates the Buyer dropdown in case the Group has changed
        group_account = form.cleaned_data['group_account']
        if int(group_account.id) != int(self.get_groupaccount_id()):
            return HttpResponseRedirect(
                '/transactions/recurring/new/' + str(group_account.id))
        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_groupaccount_id():
            context['nogroup'] = False
        else:
            context['nogroup'] = True
        return context


class EditRecurringTransactionView(FormView, BaseView):
    template_name = 'transaction/recurring/edit.html'
    form_class = EditRecurringTransactionForm
    success_url = '/transactions/recurring/0'

    def get_active_menu(self):
        return 'recurring'

    def get_form(self, form_class=EditRecurringTransactionForm):
        transaction = TransactionRecurring.objects.get(pk=self.kwargs['pk'])
        return EditRecurringTransactionForm(instance=transaction,
                                            **self.get_form_kwargs())

    def form_valid(self, form):
        super().form_valid(form)
        if form.cleaned_data['is_shared_by_all']:
            form.cleaned_data['consumers'] = UserProfile.objects.filter(
                group_accounts=form.cleaned_data['group_account'])
        form.save()
        transaction = TransactionRecurring.objects.get(pk=self.kwargs['pk'])
        modif = Modification.objects.create(
            user=UserProfile.objects.get(user=self.request.user),
            transaction_recurring=transaction)
        transaction.last_modified = modif.date
        transaction.save()
        return HttpResponseRedirect('/transactions/recurring/0')


class MyRealTransactionView(BaseView):
    template_name = "transaction/real/mytransactionsreal.html"
    context_object_name = "my real transactions"

    def get_active_menu(self):
        return 'transactions'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profile.get_show_table(self.kwargs['tableView'])
        context = super().get_context_data(**kwargs)
        transactions_real_all_sorted = TransactionReal.get_transactions_real_sorted_by_last_modified(user_profile.id)
        context['transactionsreal_all'] = transactions_real_all_sorted
        return context


class SelectGroupRealTransactionView(BaseView):
    template_name = "transaction/real/newselectgroup.html"
    context_object_name = "select transaction group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        groupaccounts = user_profile.group_accounts.all
        context['groupaccounts'] = groupaccounts
        return context


class NewRealTransactionView(FormView, BaseView):
    template_name = 'transaction/real/new.html'
    form_class = NewRealTransactionForm
    success_url = '/transactions/real/new/success/'

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

    def get_form(self, form_class=NewRealTransactionForm):
        return NewRealTransactionForm(self.get_groupaccount_id(), self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        transaction = TransactionReal.objects.get(pk=form.instance.id)
        Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction_real=transaction)
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        group_account = form.cleaned_data['group_account']
        super().form_invalid(form)
        return HttpResponseRedirect('/transactions/real/new/' + str(group_account.id))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_groupaccount_id():
            context['nogroup'] = False
        else:
            context['nogroup'] = True
        return context


class EditRealTransactionView(FormView, BaseView):
    template_name = 'transaction/real/edit.html'
    form_class = EditRealTransactionForm
    success_url = '/transactions/real/0'

    def get_active_menu(self):
        return 'transactions'

    def get_form(self, form_class=EditRealTransactionForm):
        pk = self.kwargs['pk']
        transaction = TransactionReal.objects.get(pk=pk)
        form = {}
        # prevent users that are not part of the transaction to view the form
        if self.request.user == transaction.sender.user or self.request.user == transaction.receiver.user:
            form = EditRealTransactionForm(pk, instance=transaction, **self.get_form_kwargs())
        return form

    def form_valid(self, form):
        super().form_valid(form)
        transactionreal = TransactionReal.objects.get(pk=self.kwargs['pk'])
        # prevent users that are not part of the transaction to edit the transaction
        if self.request.user == transactionreal.sender.user or self.request.user == transactionreal.receiver.user:
            form.save()
            modif = Modification.objects.create(user=UserProfile.objects.get(user=self.request.user), transaction_real=transactionreal)
            transactionreal.last_modified = modif.date
            transactionreal.save()
        return HttpResponseRedirect('/transactions/real/0')
