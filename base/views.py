from groupaccount.models import GroupAccount
from groupaccountinvite.models import GroupAccountInvite
from transaction.models import Transaction
from transactionreal.models import TransactionReal
from userprofile.models import UserProfile

from django.views.generic import TemplateView
from registration.backends.simple.views import RegistrationView

import logging
logger = logging.getLogger(__name__)


class BaseView(TemplateView):
    template_name = "base/base.html"
    context_object_name = "base"

    def get_userprofile(self):
        user = self.request.user
        return UserProfile.objects.get(user=user)

    def get_active_menu(self):
        return ''

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BaseView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            userProfile = UserProfile.objects.get(user=self.request.user)
            invites = GroupAccountInvite.objects.filter(invitee=userProfile, isAccepted=False, isDeclined=False)
            context['user'] = self.request.user
            context['userprofile'] = userProfile
            context['hasInvites'] = invites.exists()
            context['nInvites'] = invites.count()
            context['displayname'] = userProfile.displayname
            context['activeMenu'] = self.get_active_menu()
            context['isLoggedin'] = True
        return context


class NewRegistrationView(RegistrationView):

    def get_success_url(self, request, new_user):
        return '/'


class HomeView(BaseView):
    template_name = "base/index.html"
    context_object_name = "homepage"

    def get_active_menu(self):
        return 'account'

    def get_transactions(self, buyerId):
        transactions = Transaction.objects.filter(buyer__id=buyerId)
        return transactions

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        userProfile = self.get_userprofile()

        group_accounts = userProfile.group_accounts.all()
        friends = UserProfile.objects.filter(group_accounts__in=group_accounts).distinct()

        transactionsAllSorted = Transaction.get_transactions_sorted_by_last_modified(userProfile.id)
        transactionsRealAllSorted = TransactionReal.get_transactions_real_sorted_by_last_modified(userProfile.id)

        for group_account in group_accounts:
            group_account = GroupAccount.add_groupaccount_info(group_account, userProfile)

        my_total_balance_float = 0.0
        for group_account in group_accounts:
            my_total_balance_float += group_account.myBalanceFloat

        my_total_balance_str = '%.2f' % my_total_balance_float
        context['myTotalBalance'] = my_total_balance_str
        context['myTotalBalanceFloat'] = my_total_balance_float
#     invitesAllSorted = GroupAccountInvite.get_invites_sorted_by_date(userProfile)
        slowLastN = 5
#     context['invitesAll'] = invitesAllSorted[0:slowLastN]
        context['friends'] = friends
        context['transactionsAll'] = transactionsAllSorted[0:slowLastN]
        context['transactionsRealAll'] = transactionsRealAllSorted[0:slowLastN]
        context['groups'] = group_accounts
        context['homesection'] = True
        return context


class AboutView(BaseView):
    template_name = "base/about.html"
    context_object_name = "about"

    def get_active_menu(self):
        return 'about'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AboutView, self).get_context_data(**kwargs)
        context['aboutsection'] = True
        return context


class HelpView(BaseView):
    template_name = "base/help.html"
    context_object_name = "help"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HelpView, self).get_context_data(**kwargs)
        context['helpsection'] = True
        return context
