from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import StockEntry
from .models import StockEntryItem
from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User


class UserAdminCreationForm(admin_forms.AdminUserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """



class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ["client"]
        labels = {
            "client": "العميل",
        }
        widgets = {
            "client": forms.Select(attrs={
                "class": "tom-select w-full rounded-md border px-3 py-2",
            }),
        }


class StockEntryItemForm(forms.ModelForm):
    expiry_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control w-full rounded-md border px-3 py-2",
        }),
        label="تاريخ الانتهاء",
    )

    class Meta:
        model = StockEntryItem
        fields = ["product", "expiry_date", "packet_count"]
        labels = {
            "product": "المنتج",
            "expiry_date": "تاريخ الانتهاء",
            "packet_count": "عدد العلب",
        }
        widgets = {
            "product": forms.Select(attrs={
                "class": "tom-select w-full rounded-md border px-3 py-2",
            }),
            "packet_count": forms.NumberInput(attrs={
                "class": "w-full rounded-md border px-3 py-2",
            }),
        }


# Inline formset to handle multiple StockEntryItems for a StockEntry
StockEntryItemFormSet = inlineformset_factory(
    StockEntry,
    StockEntryItem,
    form=StockEntryItemForm,
    extra=1,  # number of empty forms initially shown
    can_delete=True,
)
