import logging

from django.views.generic import TemplateView

from registration.backends.simple.views import RegistrationView

from care.groupaccount.models import GroupAccount
from care.groupaccountinvite.models import GroupAccountInvite
from care.transaction.models import Transaction
from care.transaction.models import TransactionReal
from care.userprofile.models import UserProfile

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
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            user_profile = UserProfile.objects.get(user=self.request.user)
            invites = GroupAccountInvite.objects.filter(invitee=user_profile, isAccepted=False, isDeclined=False)
            context['user'] = self.request.user
            context['userprofile'] = user_profile
            context['hasInvites'] = invites.exists()
            context['nInvites'] = invites.count()
            context['displayname'] = user_profile.displayname
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

    @staticmethod
    def get_transactions(buyerId):
        transactions = Transaction.objects.filter(buyer__id=buyerId)
        return transactions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_userprofile()

        group_accounts = user_profile.group_accounts.all()
        friends = UserProfile.objects.filter(group_accounts__in=group_accounts).distinct()

        transactions_all_sorted = Transaction.get_transactions_sorted_by_last_modified(user_profile.id)
        transactionsreal_all_sorted = TransactionReal.get_transactions_real_sorted_by_last_modified(user_profile.id)

        for group_account in group_accounts:
            GroupAccount.add_groupaccount_info(group_account, user_profile)

        my_total_balance_float = 0.0
        for group_account in group_accounts:
            my_total_balance_float += group_account.my_balance_float

        my_total_balance_str = '%.2f' % my_total_balance_float
        context['my_total_balance'] = my_total_balance_str
        context['my_total_balance_float'] = my_total_balance_float
#     invitesAllSorted = GroupAccountInvite.get_invites_sorted_by_date(userProfile)
        slowlastn = 5
#     context['invitesAll'] = invitesAllSorted[0:slowLastN]
        context['friends'] = friends
        context['transactions_all'] = transactions_all_sorted[0:slowlastn]
        context['transactionsreal_all'] = transactionsreal_all_sorted[0:slowlastn]
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
        context = super().get_context_data(**kwargs)
        context['aboutsection'] = True
        return context


class HelpView(BaseView):
    template_name = "base/help.html"
    context_object_name = "help"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['helpsection'] = True
        return context
