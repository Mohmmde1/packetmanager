import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PROTECT
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import UUIDField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for packetmanager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class BaseModel(Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = DateTimeField(db_index=True, default=timezone.now)
    updated_at = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, on_delete=PROTECT)



    class Meta:
        abstract = True

class Client(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StockEntry(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiry_date = models.DateField()
    packet_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.client} - {self.product} - {self.expiry_date}"
