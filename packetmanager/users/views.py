from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from .forms import StockEntryForm
from packetmanager.users.models import User


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

    def get_object(self, queryset: QuerySet | None=None) -> User:
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
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.created_by = request.user  # assign current user here!
            stock_entry.save()
            return redirect("users:stock-entry-success")
    else:
        form = StockEntryForm()
    return render(request, "users/create_stock_entry.html", {"form": form})

def stock_entry_success(request):
    return render(request, "users/stock_entry_success.html")
