from base.views import BaseView
from groupaccount.forms import NewGroupAccountForm, EditGroupSettingForm
from groupaccount.models import GroupAccount, GroupSetting
from userprofile.models import UserProfile

from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)


class MyGroupAccountsView(BaseView):
    template_name = "groupaccount/myaccounts.html"
    context_object_name = "my groups"

    def get_active_menu(self):
        return 'group'

    def get_context_data(self, **kwargs):
        user = self.request.user
        userProfile = UserProfile.objects.get(user=user)
        userProfile.get_show_table(self.kwargs['tableView'])
        group_accounts = userProfile.group_accounts.all()

        for group_account in group_accounts:
            group_account = GroupAccount.add_groupaccount_info(group_account, userProfile)

        context = super(MyGroupAccountsView, self).get_context_data(**kwargs)
        context['groups'] = group_accounts
        context['groupssection'] = True
        return context


class NewGroupAccountView(FormView, BaseView):
    template_name = 'groupaccount/new.html'
    form_class = NewGroupAccountForm
    success_url = '/account/new/success/'

    def get_form(self, form_class):
        return NewGroupAccountForm(**self.get_form_kwargs())

    def get_active_menu(self):
        return 'group'

    def form_valid(self, form):
        super(NewGroupAccountView, self).form_valid(form)
        group_account = form.save()
        
        settings = GroupSetting()
        from userprofile.models import NotificationInterval
        if NotificationInterval.objects.get(name="Weekly"):
            settings.notification_lower_limit_interval = NotificationInterval.objects.get(name="Weekly")
        settings.save()
        group_account.settings = settings
        group_account.save()
        
        userProfile = UserProfile.objects.get(user=self.request.user)
        userProfile.group_account.add(group_account)
        userProfile.save()

        return HttpResponseRedirect('/group/new/success/')

    def get_context_data(self, **kwargs):
        context = super(NewGroupAccountView, self).get_context_data(**kwargs)

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

    def get_form(self, form_class):
        group_settings = GroupSetting.objects.get(id=self.kwargs['groupsettings_id'])
        return EditGroupSettingForm(self.request.user, instance=group_settings, **self.get_form_kwargs())

    def form_valid(self, form):
        userprofile = UserProfile.objects.get(user=self.request.user)
        super(EditGroupSettingView, self).form_valid(form)
        form.save()
        show_tablestr = "1"
        if userprofile.showTableView:
            show_tablestr = "0"
        return HttpResponseRedirect( '/group/my/' + show_tablestr)

    def get_context_data(self, **kwargs):
        context = super(EditGroupSettingView, self).get_context_data(**kwargs)
        group_settings = GroupSetting.objects.get(id=self.kwargs['groupsettings_id'])
        
        # makes sure the user is allowed to edit these group settings
        group = GroupAccount.objects.get(settings=group_settings)
        assert group in self.get_userprofile().group_account.all()
        userprofiles = UserProfile.objects.all().filter(group_accounts=group).filter(id=self.get_userprofile().id)
        if not userprofiles:
            return context
        
        form = EditGroupSettingForm(self.request.user, instance=group_settings, **self.get_form_kwargs())
        context['form'] = form
        context['group_name'] = group.name
        return context
    
