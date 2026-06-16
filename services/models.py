from django.db import models
from customers.models import Shop

#class Service(models.Model):
 #   shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

#    name = models.CharField(max_length=100)
 #   price = models.DecimalField(max_digits=8, decimal_places=2)

  #  def __str__(self):
   #     return self.name
class ServiceCategory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class ServiceItem(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='service_images/',blank=True,null=True)

    def __str__(self):
        return self.name
