import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset_confirm
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormView

from care.base.views import BaseView
from care.userprofile.forms import EditUserProfileForm, SearchUserProfileForm
from care.userprofile.models import UserProfile


class EditUserProfileView(BaseView, FormView):
    template_name = 'userprofile/edit.html'
    form_class = EditUserProfileForm
    success_url = '/'

    def get_form(self, form_class=EditUserProfileForm):
        return EditUserProfileForm(self.request.user, instance=UserProfile.objects.get(user=self.request.user), **self.get_form_kwargs())

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return HttpResponseRedirect('/userprofile/edit/success/')


class SuccessEditUserProfileView(BaseView):
    template_name = "userprofile/editsuccess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactionssection'] = True
        return context


class SearchUserProfileView(BaseView, FormView):
    template_name = 'userprofile/search.html'
    form_class = SearchUserProfileForm
    success_url = '/userprofile/search'

    def get_form(self, form_class=SearchUserProfileForm):
        return SearchUserProfileForm(**self.get_form_kwargs())

    def form_valid(self, form):
        username = form.cleaned_data['username']
        users = User.objects.filter(username__icontains=username)
        userprofiles = UserProfile.objects.filter(Q(user=users) | Q(displayname__icontains=username) | Q(firstname__icontains=username) | Q(lastname__icontains=username))
        context = super().get_context_data()
        context['has_searched'] = True
        context['searchresults'] = userprofiles
        return self.render_to_response(context)


class SendMyTransactionHistory(BaseView):
    template_name = "userprofile/historysentsuccess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprofile = UserProfile.objects.get(user=self.request.user)
        force_send = True
        userprofile.send_transaction_history(force_send)
        return context


def password_reset_confirm_custom(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='registration/password_reset_confirm.html',
                                  uidb64=uidb64, token=token, post_reset_redirect='/accounts/login/')
