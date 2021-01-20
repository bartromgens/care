from django.urls import include, path, register_converter
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

from registration.forms import RegistrationFormUniqueEmail

from care.base.views import HomeView, AboutView, HelpView, NewRegistrationView
import care.userprofile.views


class UidB64Converter:
    regex = "[0-9A-Za-z]"

    def to_python(self, val):
        return str(val)

    def to_url(self, val):
        return str(val)


register_converter(UidB64Converter, "uidb64")

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    "packages": ("recurrence",),
}

urlpatterns = [
    path("", login_required(HomeView.as_view())),
    path("help/", HelpView.as_view()),
    path("about/", AboutView.as_view()),
    path("transactions/", include("care.transaction.urls")),
    path("invites/", include("care.groupaccountinvite.urls")),
    path("userprofile/", include("care.userprofile.urls")),
    path("admin/", admin.site.urls),
    path("group/", include("care.groupaccount.urls")),
    path(
        "accounts/register/",
        NewRegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name="registration_register",
    ),  # include before the simple.urls to override register url
    path(
        "accounts/reset/confirm/<uidb64:uidb64>-<str:token>/",
        care.userprofile.views.PasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/", include("registration.backends.simple.urls")
    ),  # the django-registration module
    # Javascript i18n, as required by `django-recurrence`
    path("jsi18n/", JavaScriptCatalog.as_view(), js_info_dict),
]
