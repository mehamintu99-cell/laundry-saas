from django.contrib import admin
#from .models import Service
from .models import ServiceCategory, ServiceItem

#admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(ServiceItem)
