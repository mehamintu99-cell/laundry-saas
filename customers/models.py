from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    default_delivery_days = models.IntegerField(default=3)

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    receipt_footer = models.TextField(
        blank=True,
        default="Thank you for choosing us."
    )

    whatsapp_template = models.TextField(
        blank=True,
        default="Dear {customer}, your laundry order #{order} is ready for collection. Total Amount: {amount} OMR."
    )

    def __str__(self):
        return self.name
class Customer(models.Model):

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['shop', 'phone'],
                name='unique_customer_phone_per_shop'
            )
        ]

    def __str__(self):
        return self.name
