from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from packetmanager.users.models import Client  # Replace with your models
from packetmanager.users.models import Product  # Replace with your models

User = get_user_model()

class Command(BaseCommand):
    help = "Generate sample clients and products"

    def handle(self, *args, **kwargs):
        # Get a user to assign as created_by — e.g., the first superuser or first user
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.ERROR("No superuser found. Please create one first."))
            return

        clients = [
            "عميل ١",
            "عميل ٢",
            "عميل ٣",
            "عميل ٤",
            "عميل ٥",
        ]
        products = [
            "منتج أ",
            "منتج ب",
            "منتج ج",
            "منتج د",
            "منتج هـ",
        ]

        created_clients = 0
        created_products = 0

        for name in clients:
            obj, created = Client.objects.get_or_create(
                name=name,
                defaults={"created_by": user},
            )
            if created:
                created_clients += 1

        for name in products:
            obj, created = Product.objects.get_or_create(
                name=name,
                defaults={"created_by": user},
            )
            if created:
                created_products += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_clients} clients and {created_products} products"))
