import logging

from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormView

from care.base.views import BaseView
from care.groupaccount.forms import NewGroupAccountForm, EditGroupSettingForm
from care.groupaccount.models import GroupAccount, GroupSetting
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
            group_account = GroupAccount.add_groupaccount_info(group_account, user_profile)

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
        
        userProfile = UserProfile.objects.get(user=self.request.user)
        userProfile.group_accounts.add(group_account)
        userProfile.save()

        return HttpResponseRedirect('/group/new/success/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = NewGroupAccountForm(**self.get_form_kwargs())
        context['form'] = form
        return context


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
    
