from django.urls import path
from .views import (
    category_list,
    delete_category,
    service_list,
    delete_service,
    edit_service,
    edit_category
)

urlpatterns = [

    path(
        'categories/',
        category_list,
        name='categories'
    ),

    path(
        'category/delete/<int:category_id>/',
        delete_category,
        name='delete_category'
    ),
    path(
    'services/',
    service_list,
    name='services'),
    path(
    'service/delete/<int:service_id>/',
    delete_service,
    name='delete_service'),
    path(
    'service/edit/<int:service_id>/',
    edit_service,
    name='edit_service'),
    path(
    'category/edit/<int:category_id>/',
    edit_category,
    name='edit_category'),
]
