from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import render, redirect
from .forms import StockEntryForm, StockEntryItemFormSet
from packetmanager.users.models import User

from django.forms import modelformset_factory
from .models import StockEntry

StockEntryFormSet = modelformset_factory(StockEntry, fields=('product', 'expiry_date', 'packet_count'), extra=1)

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def create_stock_entry(request):
    if request.method == "POST":
        form = StockEntryForm(request.POST)
        formset = StockEntryFormSet(request.POST, queryset=StockEntry.objects.none())
        if form.is_valid() and formset.is_valid():
            client = form.cleaned_data['client']
            for f in formset:
                stock_entry = f.save(commit=False)
                stock_entry.client = client
                stock_entry.created_by = request.user
                stock_entry.save()
            return redirect("users:stock-entry-success")
    else:
        form = StockEntryForm()
        formset = StockEntryFormSet(queryset=StockEntry.objects.none())
    return render(request, "users/create_stock_entry.html", {"form": form, "formset": formset})

def stock_entry_success(request):
    return render(request, "users/stock_entry_success.html")
