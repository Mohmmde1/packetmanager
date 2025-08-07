from django.urls import path

from .views import create_stock_entry
from .views import stock_entry_success
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("create-stock-entry/", view=create_stock_entry, name="create-stock-entry"),
    path("stock-entry-success/", view=stock_entry_success, name="stock-entry-success"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
