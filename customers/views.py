from django.shortcuts import render, redirect
from .models import Customer
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib import messages
from django.shortcuts import get_object_or_404


@login_required
def customer_list(request):

    search = request.GET.get('search', '')

    customers = Customer.objects.filter(
        shop=request.user.shop
    )

    if search:

        customers = customers.filter(
            name__icontains=search
        ) | Customer.objects.filter(
            shop=request.user.shop,
            phone__icontains=search
        )

    customers = customers.order_by('name')

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': customers,
            'search': search
        }
    )

@login_required
def add_customer(request):

    if request.method == "POST":
        phone = request.POST.get("phone")
        existing_customer = Customer.objects.filter(shop=request.user.shop,phone=phone).first()

        if existing_customer:

            return render(
                request,
                'customers/add_customer.html',
                {
                    'error': 'A customer with this phone number already exists.',
                    'name': request.POST.get("name"),
                    'phone': phone
                }
            )
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        if not name:
            return render(
                request,
                'customers/add_customer.html',
                {
                'error': 'Customer name is required.',
                'name': name,
                'phone': phone
                }
            )
        if not phone:
            return render(
                request,
                'customers/add_customer.html',
                {
                    'error': 'Phone number is required.',
                    'name': name,
                    'phone': phone
                }
            )

        Customer.objects.create(
            shop=request.user.shop,
            name=request.POST.get("name"),
            phone=request.POST.get("phone")
        )

        return redirect('/customers/')

    return render(
        request,
        'customers/add_customer.html'
    )

@login_required
def customer_detail(request, customer_id):

    customer = Customer.objects.get(
        id=customer_id,
        shop=request.user.shop
    )

    orders = Order.objects.filter(
        customer=customer
    ).order_by('-id')
    all_orders = orders
    last_visit = orders.first()

    total_orders = orders.count()

    total_spent = sum(
        order.total_amount
        for order in orders
    )
    outstanding_amount = sum(
        order.balance
        for order in orders
    )

    return render(
        request,
        'customers/customer_detail.html',
        {
            'customer': customer,
            'orders': orders,
            'total_orders': total_orders,
            'total_spent': total_spent,
            'last_visit': last_visit,
            'all_orders': all_orders,
            'outstanding_amount': outstanding_amount
        }
    )
@login_required
def shop_settings(request):

    shop = request.user.shop

    if request.method == "POST":

        shop.name = request.POST.get("name")
        shop.phone = request.POST.get("phone")
        shop.address = request.POST.get("address")
        shop.receipt_footer = request.POST.get("receipt_footer")
        shop.whatsapp_template = request.POST.get("whatsapp_template")
        shop.default_delivery_days = request.POST.get("default_delivery_days",3)

        shop.save()
        messages.success(request,"Settings saved successfully.")
        return redirect('/settings/')

    return render(
        request,
        'customers/shop_settings.html',
        {
            'shop': shop
        }
    )
@login_required
def edit_customer(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id,
        shop=request.user.shop
    )

    if request.method == "POST":

       
        name = request.POST.get("name").strip()
        phone = request.POST.get("phone").strip()
        if not name:
            return render(
                request,
                'customers/edit_customer.html',
                {
                    'customer': customer,
                    'error': 'Customer name is required.'
                }
            )
        if not phone:
            return render(
                request,
                'customers/edit_customer.html',
                {
                    'customer': customer,
                    'error': 'Phone number is required.'
                }
            )

        existing_customer = Customer.objects.filter(
            shop=request.user.shop,
            phone=phone
        ).exclude(
            id=customer.id
        ).first()

        if existing_customer:

            return render(
                request,
                'customers/edit_customer.html',
                {
                    'customer': customer,
                    'error': 'A customer with this phone number already exists.'
                }
            )

        customer.name = name
        customer.phone = phone

        customer.save()

        return redirect(
            f'/customer/{customer.id}/'
        )

    return render(
        request,
        'customers/edit_customer.html',
        {
            'customer': customer
        }
    )
