from rest_framework import permissions
from rest_framework import status

# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from packetmanager.users.models import Client
from packetmanager.users.models import Product
from packetmanager.users.models import StockEntry
from packetmanager.users.models import User

from .serializers import ClientSerializer
from .serializers import ProductSerializer
from .serializers import StockEntrySerializer
from .serializers import UserSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockEntryViewSet(viewsets.ModelViewSet):
    serializer_class = StockEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StockEntry.objects.filter(created_by=self.request.user)
