from django.urls import path
from .views import find_customer
from .views import logout_view
from .views import dashboard, new_order, orders_list, order_detail,update_status,customer_search, reports,receive_payment,edit_notes,outstanding_payments,customer_outstanding_report,overdue_orders,orders_due_today,ready_orders,pending_orders_view,service_summary,payment_report,daily_closing,partial_delivery,login_view,expense_list,delete_expense,edit_expense,expense_report,profit_report,shop_list,add_shop,edit_shop,reset_shop_password,deactivate_shop,edit_order


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('new-order/', new_order, name='new_order'),
    path('orders/', orders_list, name='orders_list'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('order/<int:order_id>/status/<str:status>/',update_status,name='update_status'),
    path('customer-search/',customer_search,name='customer_search'),
    path(
    'find-customer/',
    find_customer,
    name='find_customer'),
    path(
    'reports/',
    reports,
    name='reports'),
    path(
    'order/<int:order_id>/payment/',
    receive_payment,
    name='receive_payment'),
    path(
    'order/<int:order_id>/notes/',
    edit_notes,
    name='edit_notes'),
    path(
    'outstanding-payments/',
    outstanding_payments,
    name='outstanding_payments'),
    path(
    'customer-outstanding/',
    customer_outstanding_report,
    name='customer_outstanding_report'),
    path(
    'overdue-orders/',
    overdue_orders,
    name='overdue_orders'),
    path(
    'orders-due-today/',
    orders_due_today,
    name='orders_due_today'),
    path(
    'ready-orders/',
    ready_orders,
    name='ready_orders'),
    path(
    'pending-orders/',
    pending_orders_view,
    name='pending_orders'),
    path(
    'service-summary/',
    service_summary,
    name='service_summary'),
    path(
    'payment-report/',
    payment_report,
    name='payment_report'),
    path(
    'daily-closing/',
    daily_closing,
    name='daily_closing'),
    path(
    'order/<int:order_id>/deliver/',
    partial_delivery,
    name='partial_delivery'),
    path(
    'logout/',
    logout_view,
    name='logout'),
    path(
    'login/',
    login_view,
    name='login'),
    path(
    'expenses/',
    expense_list,
    name='expenses'
),
    path(
    'expense/delete/<int:expense_id>/',
    delete_expense,
    name='delete_expense'
),
    path(
    'expense/edit/<int:expense_id>/',
    edit_expense,
    name='edit_expense'
),
    path(
    'expense-report/',
    expense_report,
    name='expense_report'
),
    path(
    'profit-report/',
    profit_report,
    name='profit_report'
),
    path(
    'shops/',
    shop_list,
    name='shop_list'
),
    path(
    'shops/add/',
    add_shop,
    name='add_shop'
),
    path(

    'shops/<int:shop_id>/edit/',

    edit_shop,

    name='edit_shop'

),
    path(

    'shops/<int:shop_id>/reset-password/',

    reset_shop_password,

    name='reset_shop_password'

),
    path(

    'shops/<int:shop_id>/delete/',

    deactivate_shop,

    name='deactivate_shop'

),
    path(
    'order/<int:order_id>/edit/',
    edit_order,
    name='edit_order'
),
    
    
]
