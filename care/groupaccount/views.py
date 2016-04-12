import logging

from django.db.models import Sum
from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormView

from care.base.views import BaseView
from care.groupaccount.forms import NewGroupAccountForm, EditGroupSettingForm
from care.groupaccount.models import GroupAccount, GroupSetting
from care.transaction.models import Transaction
from care.userprofile.models import UserProfile

logger = logging.getLogger(__name__)


class MyGroupAccountsView(BaseView):
    template_name = "groupaccount/myaccounts.html"
    context_object_name = "my groups"

    def get_active_menu(self):
        return 'group'

    def get_context_data(self, **kwargs):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        user_profile.get_show_table(self.kwargs['tableView'])
        group_accounts = user_profile.group_accounts.all()
        for group_account in group_accounts:
            GroupAccount.add_groupaccount_info(group_account, user_profile)
        context = super().get_context_data(**kwargs)
        context['groups'] = group_accounts
        context['groupssection'] = True
        return context


class NewGroupAccountView(FormView, BaseView):
    template_name = 'groupaccount/new.html'
    form_class = NewGroupAccountForm
    success_url = '/account/new/success/'

    def get_form(self, form_class=NewGroupAccountForm):
        return NewGroupAccountForm(**self.get_form_kwargs())

    def get_active_menu(self):
        return 'group'

    def form_valid(self, form):
        super().form_valid(form)
        group_account = form.save()
        
        settings = GroupSetting()
        from care.userprofile.models import NotificationInterval
        if NotificationInterval.objects.get(name="Weekly"):
            settings.notification_lower_limit_interval = NotificationInterval.objects.get(name="Weekly")
        settings.save()
        group_account.settings = settings
        group_account.save()
        
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_profile.group_accounts.add(group_account)
        user_profile.save()

        return HttpResponseRedirect('/group/new/success/')


class SucessNewGroupAccountView(BaseView):
    template_name = 'groupaccount/newsuccess.html'

    def get_active_menu(self):
        return 'accounts'


class EditGroupSettingView(BaseView, FormView):
    template_name = 'groupaccount/settings.html'
    form_class = EditGroupSettingForm
    success_url = '/'

    def get_form(self, form_class=EditGroupSettingForm):
        group_settings = GroupSetting.objects.get(id=self.kwargs['groupsettings_id'])
        return EditGroupSettingForm(self.request.user, instance=group_settings, **self.get_form_kwargs())

    def form_valid(self, form):
        userprofile = UserProfile.objects.get(user=self.request.user)
        super().form_valid(form)
        form.save()
        show_tablestr = "1"
        if userprofile.showTableView:
            show_tablestr = "0"
        return HttpResponseRedirect( '/group/my/' + show_tablestr)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_settings = GroupSetting.objects.get(id=self.kwargs['groupsettings_id'])

        # makes sure the user is allowed to edit these group settings
        group = GroupAccount.objects.get(settings=group_settings)
        assert group in self.get_userprofile().group_accounts.all()
        userprofiles = UserProfile.objects.all().filter(group_accounts=group).filter(id=self.get_userprofile().id)
        if not userprofiles:
            return context
        
        form = EditGroupSettingForm(self.request.user, instance=group_settings, **self.get_form_kwargs())
        context['form'] = form
        context['group_name'] = group.name
        return context


class StatisticsGroupAccount(BaseView):
    template_name = "groupaccount/statistics.html"

    def get_active_menu(self):
        return 'accounts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_account_id = kwargs['groupaccount_id']
        group = GroupAccount.objects.get(id=group_account_id)
        group_users = UserProfile.objects.filter(group_accounts=group.id)
        if UserProfile.objects.get(user=self.request.user) not in group_users:
            return context

        for user in group_users:
            user.balance = UserProfile.get_balance(group.id, user.id)
            user.n_trans_buyer = Transaction.objects.filter(buyer=user).count()
            user.n_trans_consumer = Transaction.objects.filter(consumers=user).count()
            amount__sum = Transaction.get_buyer_transactions(user.id).aggregate(Sum('amount'))['amount__sum']
            if amount__sum:
                user.total_bought = float(amount__sum)
            consumer_transactions = Transaction.get_consumer_transactions(user.id)
            total_consumed = 0.0
            for transaction in consumer_transactions:
                total_consumed += float(transaction.amount/transaction.consumers.count())
            user.total_consumed = total_consumed
        turnover = 0
        for user in group_users:
            turnover += user.total_bought
        context['users'] = group_users
        context['group_name'] = group.name
        context['turnover'] = turnover
        return context