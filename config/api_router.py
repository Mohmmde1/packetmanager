from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from packetmanager.users.api.views import ProductViewSet
from packetmanager.users.api.views import StockEntryViewSet
from packetmanager.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register(r"products", ProductViewSet)
router.register(r"stock-entries", StockEntryViewSet)

app_name = "api"
urlpatterns = router.urls
