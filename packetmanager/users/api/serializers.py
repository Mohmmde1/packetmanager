from rest_framework import serializers

from packetmanager.users.models import Client
from packetmanager.users.models import Product
from packetmanager.users.models import StockEntry
from packetmanager.users.models import StockEntryItem
from packetmanager.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class StockEntryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockEntryItem
        fields = ["id", "product", "expiry_date", "packet_count"]


class StockEntrySerializer(serializers.ModelSerializer):
    items = StockEntryItemSerializer(many=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = StockEntry
        fields = ["id", "client", "created_by", "items", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        stock_entry = StockEntry.objects.create(**validated_data)
        for item in items_data:
            StockEntryItem.objects.create(stock_entry=stock_entry, **item)
        return stock_entry
