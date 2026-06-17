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
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,related_name='services')

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='service_images/',blank=True,null=True)
    icon = models.CharField(max_length=50,blank=True,default='')
    def save(self, *args, **kwargs):

        ICON_MAP = {

            'shirt':'shirt.png',

            'pants':'pants.png',

            'blanket':'blanket.png',

            'dishdasha':'dishdasha.png',

            'saree':'saree.png',

            'salwar':'salwar.png',

            'abaya':'abaya.png',

            'jacket':'jacket.png',

            'shall':'shall.png',

            'bed sheet':'bedsheet.png'

        }

        if not self.icon:

            key = self.name.lower().strip()

            if key in ICON_MAP:

                self.icon = ICON_MAP[key]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
