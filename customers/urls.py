from django.urls import path
from .views import customer_list, add_customer
from .views import shop_settings
from .views import (
    customer_list,
    add_customer,
    customer_detail,
    edit_customer
)

urlpatterns = [

    path(
        'customers/',
        customer_list,
        name='customer_list'
    ),

    path(
        'add-customer/',
        add_customer,
        name='add_customer'
    ),
    path(
        'customer/<int:customer_id>/',
        customer_detail,
        name='customer_detail'
),
    path(
    'settings/',
    shop_settings,
    name='shop_settings'
),
    path(
    'customer/edit/<int:customer_id>/',
    edit_customer,
    name='edit_customer'
),

]
