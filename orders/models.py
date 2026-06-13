from django.db import models
from customers.models import Shop, Customer
from services.models import ServiceItem

class Order(models.Model):

    STATUS_CHOICES = [
    ('received', 'Received'),
    ('ready', 'Ready'),
    ('partial', 'Partially Picked Up'),
    ('picked', 'Delivered'),]
    

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_date = models.DateField(
    null=True,
    blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    notes = models.TextField(blank=True,null=True)
    amount_paid = models.DecimalField(max_digits=10,decimal_places=3,default=0)

    payment_status = models.CharField(max_length=20,default='unpaid')

    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    #service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)
    delivered_quantity = models.IntegerField(default=0)

    price = models.DecimalField(max_digits=10, decimal_places=3)
    @property
    def pending_quantity(self):
        return self.quantity - self.delivered_quantity

    def __str__(self):
        return self.service.name
class Payment(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.order.id} - {self.amount}"
class Expense(models.Model):

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    expense_date = models.DateField()

    category = models.CharField(
        max_length=100
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
