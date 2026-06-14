
from django.shortcuts import render, redirect
from .models import Customer
from services.models import ServiceItem
from services.models import ServiceCategory, ServiceItem
from .models import Order, OrderItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from django.contrib.auth.models import User
from customers.models import Shop
from django.db.models import Sum
from customers.models import Customer
from django.http import JsonResponse
from customers.models import Customer
from django.db.models import Sum
from openpyxl import Workbook
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Sum, F,DecimalField
from .models import (Customer,Order,OrderItem,ServiceItem,Shop,Payment)
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .models import Expense
from urllib.parse import quote
from django.db import transaction
from customers.models import Subscription




#from .models import Customer

@login_required
def dashboard(request):

    shop = request.user.shop
    total_orders = Order.objects.filter(shop=shop).count()
    total_customers = Customer.objects.filter(shop=shop).count()

    pending_orders = Order.objects.filter(shop=shop,status='received').count()
    ready_orders = Order.objects.filter(shop=shop,status='ready').count()
    overdue_orders = Order.objects.filter(shop=shop,delivery_date__lt=date.today()).exclude(status='picked').count()
    today_revenue = Order.objects.filter(shop=shop,created_at__date=date.today()).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    current_month = date.today().month
    current_year = date.today().year
    month_revenue = Order.objects.filter(shop=shop,created_at__month=current_month,created_at__year=current_year).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_customers = Customer.objects.filter(shop=shop).count()
    outstanding_amount = 0
    today_orders = Order.objects.filter(shop=shop,delivery_date=date.today()).exclude(status='picked').count()
    today_date = date.today().strftime('%Y-%m-%d')

    month_start = date(date.today().year,date.today().month,1).strftime('%Y-%m-%d')
    unpaid_orders = Order.objects.filter(shop=shop).exclude(payment_status='paid')
    picked_orders = Order.objects.filter(shop=shop,status='picked').count()
    today_collections = Payment.objects.filter(
    order__shop=request.user.shop,payment_date__date=timezone.now().date()).aggregate(total=Sum('amount'))['total'] or 0
    for order in unpaid_orders:
        outstanding_amount += order.balance

    return render(
        request,
        'orders/dashboard.html',
        {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'ready_orders': ready_orders,
            'overdue_orders': overdue_orders,
            'today_revenue': today_revenue,
            'month_revenue': month_revenue,
            'total_customers': total_customers,
            'outstanding_amount': outstanding_amount,
            'total_customers': total_customers,
            'today_orders': today_orders,
            'today_date': today_date,
            'month_start': month_start,
            'picked_orders': picked_orders,
            'today_collections': today_collections,
        }
    )

    return render(request, 'orders/dashboard.html', context)
@login_required
def new_order(request):

    shop = request.user.shop
    customers = Customer.objects.filter(shop=shop)
    
    categories = ServiceCategory.objects.filter(shop=shop)
    default_date = timezone.now().date() + timedelta(days=request.user.shop.default_delivery_days)

    if request.method == "POST":

        phone = request.POST.get("phone")
        customer_name = request.POST.get("customer_name")
        delivery_date = request.POST.get('delivery_date') or default_date
        customer, created = Customer.objects.get_or_create(
        shop=request.user.shop,
        phone=phone,
        defaults={'name': customer_name})
        #delivery_date = request.POST.get('delivery_date')
        

        order = Order.objects.create(
            shop=customer.shop,
            customer=customer,
            delivery_date=delivery_date,
            status='received',
            total_amount=0
        )

        total = 0

        items = ServiceItem.objects.all()

        for item in items:

            qty = int(request.POST.get(f"item_{item.id}", 0))

            if qty > 0:

                OrderItem.objects.create(
                    order=order,
                    service=item,
                    quantity=qty,
                    price=item.price
                )

                total += qty * float(item.price)
        if total == 0:
            order.delete()
            return render(
                request,
                'orders/new_order.html',
                {
                    'customers': customers,
                    'categories': categories,
                    'default_date': default_date,
                    'error': 'Please select at least one service.'
                }
            )

        order.total_amount = total
        order.save()

        #return redirect(f'/order/{order.id}/')
        return redirect(f'/order/{order.id}/?new=1')

    return render(
        request,
        'orders/new_order.html',
        {
            'customers': customers,
            'categories': categories,
            'default_date': default_date
        }
    )
#@login_required
#def orders_list(request):

 #   orders = Order.objects.all().order_by('-id')

  #  return render(
   #     request,
    #    'orders/orders_list.html',
     #   {
      #      'orders': orders
       # }
    #)
@login_required
def order_detail(request, order_id):
    
    shop = request.user.shop
    order = Order.objects.get(id=order_id,shop=shop)
    is_new_order = request.GET.get('new') == '1'
    is_ready_order = request.GET.get('ready') == '1'
    items = OrderItem.objects.filter(order=order)
    payments = Payment.objects.filter(order=order).order_by('-payment_date')
    for item in items:
        item.line_total = item.quantity * item.price
    receipt_text = f"""
{shop.name}

Order Created Successfully

Order No: {order.id}

Customer: {order.customer.name}

Phone: {order.customer.phone}

--------------------------------

Items:
"""

    for item in items:

        receipt_text += (
            f"\n{item.service.name}"
            f" x {item.quantity}"
            f" = {item.line_total:.3f} OMR"
        )

    receipt_text += f"""

--------------------------------

Total Amount: {order.total_amount:.3f} OMR

Delivery Date: {order.delivery_date}

Thank you for choosing {shop.name}.
"""
    ready_text = f"""
{shop.name}

Dear {order.customer.name},

Your order #{order.id} is now ready for collection.

Items:
"""

    for item in items:

        ready_text += (
            f"\n"
            f"{item.service.name}"
            f" x {item.quantity}"
            f" = {item.line_total:.3f} OMR"
        )

    ready_text += f"""

--------------------------------

Total Amount:

{order.total_amount:.3f} OMR

Please visit our shop to collect your order.

Thank you for choosing

{shop.name}
"""
    whatsapp_url = (f"https://web.whatsapp.com/send"f"?phone=968{order.customer.phone}"f"&text={quote(receipt_text)}")
    ready_whatsapp_url = (f"https://web.whatsapp.com/send"f"?phone=968{order.customer.phone}"f"&text={quote(ready_text)}")
    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
            'items': items,
            'shop': shop,
            'print_mode': False,
            'payments': payments,
            'is_new_order': is_new_order,
            'whatsapp_url': whatsapp_url,
            'is_ready_order': is_ready_order,
            'ready_whatsapp_url': ready_whatsapp_url
        }
    )
@login_required
def update_status(request, order_id, status):

    shop = request.user.shop
    order = Order.objects.get(id=order_id,shop=shop)

    order.status = status
    if status == "picked":

        items = OrderItem.objects.filter(order=order)

        for item in items:

            item.delivered_quantity = item.quantity

            item.save()
    order.save()
    if status == "ready":
        return redirect(f'/order/{order.id}/?ready=1')

    return redirect(f'/order/{order.id}/')



@login_required
def orders_list(request):

    shop = request.user.shop

    search = request.GET.get('search', '')

    orders = Order.objects.filter(
        shop=shop
    ).order_by('-id')

    if search:

        orders = orders.filter(
            Q(customer__name__icontains=search) |
            Q(customer__phone__icontains=search)
        )

    return render(
        request,
        'orders/orders_list.html',
        {
            'orders': orders,
            'search': search
        }
    )
@login_required
def customer_search(request):

    customer = None

    phone = request.POST.get("phone") or request.GET.get("phone")
    if phone:

        

        try:

            customer = Customer.objects.get(
                phone=phone,
                shop=request.user.shop
            )

        except Customer.DoesNotExist:

            customer = None

    return render(
        request,
        'orders/customer_search.html',
        {
            'customer': customer
        }
    )


@login_required
def find_customer(request):

    phone = request.GET.get('phone')

    try:

        customer = Customer.objects.get(
            shop=request.user.shop,
            phone=phone
        )

        return JsonResponse({
            'found': True,
            'name': customer.name
        })

    except Customer.DoesNotExist:

        return JsonResponse({
            'found': False
        })


@login_required
def reports(request):

    export = request.GET.get('export')

    report_items = []
    total_revenue = 0

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    customer_id = request.GET.get('customer')

    customers = Customer.objects.filter(
        shop=request.user.shop
    ).order_by('name')

    if from_date and to_date:

        report_items = OrderItem.objects.filter(
            order__shop=request.user.shop,
            order__created_at__date__range=[
                from_date,
                to_date
            ]
        ).select_related(
            'order',
            'service',
            'service__category'
        )

        if customer_id and customer_id != "all":

            report_items = report_items.filter(
                order__customer_id=customer_id
            )

        for item in report_items:

            item.line_total = item.quantity * item.price

        total_revenue = sum(
            item.line_total
            for item in report_items
        )

        if export == "excel":

            wb = Workbook()
            ws = wb.active

            ws.title = "Laundry Report"

            ws.append([
                "Date",
                "Order No",
                "Customer",
                "Category",
                "Service",
                "Quantity",
                "Amount"
            ])

            for item in report_items:

                ws.append([
                    item.order.created_at.strftime("%d-%m-%Y"),
                    item.order.id,
                    item.order.customer.name,
                    item.service.category.name,
                    item.service.name,
                    item.quantity,
                    float(item.line_total)
                ])

            ws.append([])

            ws.append([
                "",
                "",
                "",
                "",
                "",
                "Total Revenue",
                float(total_revenue)
            ])

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            response['Content-Disposition'] = (
                'attachment; filename=laundry_report.xlsx'
            )

            wb.save(response)

            return response

    return render(
        request,
        'orders/reports.html',
        {
            'report_items': report_items,
            'total_revenue': total_revenue,
            'from_date': from_date,
            'to_date': to_date,
            'customers': customers,
            'customer_id': customer_id
        }
    )
@login_required
def receive_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        shop=request.user.shop
    )

    if request.method == "POST":

        amount = Decimal(
            request.POST.get('amount', '0')
        )
        if amount > order.balance:

            return render(
                request,
                'orders/receive_payment.html',
                {
                    'order': order,
                    'error': 'Payment cannot exceed outstanding balance.'
                }
            )
        if amount <= 0:

            return render(
                request,
                'orders/receive_payment.html',
                {
                    'order': order,
                    'error': 'Payment amount must be greater than zero.'
                }
            )

        order.amount_paid += amount
        Payment.objects.create(order=order,amount=amount)

        if order.amount_paid >= order.total_amount:

            order.payment_status = 'paid'

        else:

            order.payment_status = 'partial'

        order.save()

        return redirect(
            f'/order/{order.id}/'
        )

    return render(
        request,
        'orders/receive_payment.html',
        {
            'order': order
        }
    )
@login_required
def edit_notes(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        shop=request.user.shop
    )

    if request.method == "POST":

        order.notes = request.POST.get(
            'notes',
            ''
        )

        order.save()

        return redirect(
            f'/order/{order.id}/'
        )

    return render(
        request,
        'orders/edit_notes.html',
        {
            'order': order
        }
    )
@login_required
def outstanding_payments(request):

    shop = request.user.shop

    orders = Order.objects.filter(
        shop=shop
    ).exclude(
        payment_status='paid'
    )

    total_outstanding = 0

    for order in orders:

        total_outstanding += order.balance

    return render(
        request,
        'orders/outstanding_payments.html',
        {
            'orders': orders,
            'total_outstanding': total_outstanding
        }
    )


@login_required
def customer_outstanding_report(request):

    shop = request.user.shop

    customers = Customer.objects.filter(
        shop=shop
    )

    report = []
    total_outstanding = 0

    for customer in customers:

        orders = Order.objects.filter(
            customer=customer
        ).exclude(
            payment_status='paid'
        )

        outstanding = sum(
            order.balance
            for order in orders
        )

        if outstanding > 0:

            report.append({
                'customer': customer,
                'outstanding': outstanding
            })

            total_outstanding += outstanding

    return render(
        request,
        'orders/customer_outstanding_report.html',
        {
            'report': report,
            'total_outstanding': total_outstanding
        }
    )
@login_required
def overdue_orders(request):

    shop = request.user.shop

    orders = Order.objects.filter(
        shop=shop,
        delivery_date__lt=date.today()
    ).exclude(
        status='picked'
    ).order_by('delivery_date')

    return render(
        request,
        'orders/overdue_orders.html',
        {
            'orders': orders
        }
    )
@login_required
def orders_due_today(request):

    shop = request.user.shop

    orders = Order.objects.filter(
        shop=shop,
        delivery_date=date.today()
    ).exclude(
        status='picked'
    ).order_by('id')

    return render(
        request,
        'orders/orders_due_today.html',
        {
            'orders': orders
        }
    )
@login_required
def ready_orders(request):

    shop = request.user.shop

    orders = Order.objects.filter(
        shop=shop,
        status='ready'
    ).order_by('-id')

    return render(
        request,
        'orders/ready_orders.html',
        {
            'orders': orders
        }
    )
@login_required
def pending_orders_view(request):

    shop = request.user.shop

    orders = Order.objects.filter(
        shop=shop,
        status='received'
    ).order_by('-id')

    return render(
        request,
        'orders/pending_orders.html',
        {
            'orders': orders
        }
    )
@login_required
def service_summary(request):

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    summary = []

    if from_date and to_date:

        items = OrderItem.objects.filter(
            order__shop=request.user.shop,
            order__created_at__date__range=[
                from_date,
                to_date
            ]
        )

        services = {}

        for item in items:

            service_name = item.service.name

            revenue = item.quantity * item.price

            if service_name not in services:

                services[service_name] = {
                    'quantity': 0,
                    'revenue': 0
                }

            services[service_name]['quantity'] += item.quantity
            services[service_name]['revenue'] += revenue

        summary = sorted(services.items(),key=lambda x: x[1]['revenue'],reverse=True)

    return render(
        request,
        'orders/service_summary.html',
        {
            'summary': summary,
            'from_date': from_date,
            'to_date': to_date
        }
    )
@login_required
def payment_report(request):

    payments = Payment.objects.filter(
        order__shop=request.user.shop
    ).select_related(
        'order',
        'order__customer'
    )

    total_collected = 0

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Dashboard card: Today's Collections
    if request.GET.get('today'):

        today = timezone.now().date()

        payments = payments.filter(
            payment_date__date=today
        )

        from_date = today
        to_date = today

    elif from_date and to_date:

        payments = payments.filter(
            payment_date__date__range=[
                from_date,
                to_date
            ]
        )

    else:

        payments = Payment.objects.none()

    total_collected = sum(
        payment.amount
        for payment in payments
    )

    return render(
        request,
        'orders/payment_report.html',
        {
            'payments': payments,
            'total_collected': total_collected,
            'from_date': from_date,
            'to_date': to_date
        }
    )
@login_required
def daily_closing(request):

    report_date = request.GET.get('date')

    if report_date:
        selected_date = report_date
    else:
        selected_date = timezone.now().date()

    orders_received = Order.objects.filter(
        shop=request.user.shop,
        created_at__date=selected_date
    ).count()

    orders_ready = Order.objects.filter(
        shop=request.user.shop,
        status='ready',
        created_at__date=selected_date
    ).count()

    orders_picked = Order.objects.filter(
        shop=request.user.shop,
        status='picked',
        created_at__date=selected_date
    ).count()

    revenue_generated = Order.objects.filter(
        shop=request.user.shop,
        created_at__date=selected_date
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    payments_collected = Payment.objects.filter(
        order__shop=request.user.shop,
        payment_date__date=selected_date
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    outstanding_balance = Order.objects.filter(
        shop=request.user.shop).aggregate(total=Sum('total_amount'))['total'] or 0
    total_paid = Order.objects.filter(
        shop=request.user.shop).aggregate(total=Sum('amount_paid'))['total'] or 0
    outstanding_balance = outstanding_balance - total_paid

    return render(
        request,
        'orders/daily_closing.html',
        {
            'selected_date': selected_date,
            'orders_received': orders_received,
            'orders_ready': orders_ready,
            'orders_picked': orders_picked,
            'revenue_generated': revenue_generated,
            'payments_collected': payments_collected,
            'outstanding_balance': outstanding_balance,
        }
    )
@login_required
def partial_delivery(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        shop=request.user.shop
    )

    items = OrderItem.objects.filter(
        order=order
    )

    if request.method == "POST":

        for item in items:

            qty = int(
                request.POST.get(
                    f'item_{item.id}',
                    0
                )
            )

            max_allowed = (
                item.quantity -
                item.delivered_quantity
            )

            qty = min(qty, max_allowed)

            item.delivered_quantity += qty

            item.save()
        all_delivered = True
        for item in items:

            if item.pending_quantity > 0:

                all_delivered = False
                break

        if all_delivered:

            order.status = 'picked'
            order.save()

        return redirect(
            f'/order/{order.id}/'
        )

    return render(
        request,
        'orders/partial_delivery.html',
        {
            'order': order,
            'items': items
        }
    )
def logout_view(request):

    logout(request)

    return redirect('/login/')
def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            # Super admin can always login
            if user.is_superuser:
                login(request, user)
                return redirect('/')

            # Laundry shop users
            if hasattr(user, 'shop'):

                if not user.shop.is_active:

                    messages.error(

                        request,
                        'Your account is inactive. Please contact administrator.'
                    )

                    return redirect('/login/')


            login(request, user)

            return redirect('/')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'orders/login.html'
    )
@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        shop=request.user.shop
    ).order_by('-expense_date')

    if request.method == "POST":

        amount = float(
            request.POST.get('amount', 0)
        )

        if amount <= 0:

            return render(
                request,
                'orders/expenses.html',
                {
                    'expenses': expenses,
                    'error': 'Expense amount must be greater than zero.'
                }
            )

        Expense.objects.create(

            shop=request.user.shop,

            expense_date=request.POST.get(
                'expense_date'
            ),

            category=request.POST.get(
                'category'
            ),

            description=request.POST.get(
                'description'
            ),

            amount=amount
        )

        return redirect('/expenses/')

    return render(
        request,
        'orders/expenses.html',
        {
            'expenses': expenses
        }
    )
@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        shop=request.user.shop
    )

    expense.delete()

    return redirect('/expenses/')
@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        shop=request.user.shop
    )

    if request.method == "POST":

        expense.expense_date = request.POST.get(
            'expense_date'
        )

        expense.category = request.POST.get(
            'category'
        )

        expense.description = request.POST.get(
            'description'
        )

        expense.amount = request.POST.get(
            'amount'
        )

        expense.save()

        return redirect('/expenses/')

    return render(
        request,
        'orders/edit_expense.html',
        {
            'expense': expense
        }
    )
@login_required
def expense_report(request):

    expenses = Expense.objects.none()

    total_expenses = 0

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:

        expenses = Expense.objects.filter(
            shop=request.user.shop,
            expense_date__range=[
                from_date,
                to_date
            ]
        )

        total_expenses = sum(
            expense.amount
            for expense in expenses
        )

    return render(
        request,
        'orders/expense_report.html',
        {
            'expenses': expenses,
            'total_expenses': total_expenses,
            'from_date': from_date,
            'to_date': to_date
        }
    )
@login_required
def profit_report(request):

    revenue = 0
    expenses = 0
    profit = 0
    outstanding = 0
    cash_profit = 0
    

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:

        revenue = Order.objects.filter(
            shop=request.user.shop,
            created_at__date__range=[
                from_date,
                to_date
            ]
        ).aggregate(
            Sum('total_amount')
        )['total_amount__sum'] or 0

        expenses = Expense.objects.filter(
            shop=request.user.shop,
            expense_date__range=[
                from_date,
                to_date
            ]
        ).aggregate(
            Sum('amount')
        )['amount__sum'] or 0

        profit = revenue - expenses
        outstanding = sum(
            order.balance
            for order in Order.objects.filter(
                shop=request.user.shop,
                created_at__date__range=[
                    from_date,
                    to_date
                ]
            ).exclude(
                payment_status='paid'
            )
        )

        cash_profit = profit - outstanding

    return render(
        request,
        'orders/profit_report.html',
        {
            'revenue': revenue,
            'expenses': expenses,
            'profit': profit,
            'from_date': from_date,
            'to_date': to_date,
            'outstanding': outstanding,
            'cash_profit': cash_profit
        }
    )
@login_required
def shop_list(request):

    if not request.user.is_superuser:

        return redirect('/')

    shops = Shop.objects.all().order_by('name')
    for shop in shops:
        shop.customer_count = shop.customer_set.count()
        shop.order_count = shop.order_set.count()
        shop.outstanding = sum(
            order.balance
            for order in shop.order_set.all()

        )


    return render(

        request,
        'orders/shops.html',
        {
            'shops': shops
        }
    )
@login_required
def add_shop(request):

    if not request.user.is_superuser:
        return redirect('/')

    if request.method == "POST":

        username = request.POST.get('username')

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'orders/add_shop.html',
                {
                    'error': 'Username already exists.'
                }
            )

        with transaction.atomic():

            user = User.objects.create_user(

                username=username,

                password=request.POST.get('password')

            )

            shop = Shop.objects.create(

                user=user,

                name=request.POST.get('name'),

                phone=request.POST.get('phone'),

                address=request.POST.get('address'),

                default_delivery_days=int(

                    request.POST.get(
                        'default_delivery_days'
                    ) or 2

                )

            )

            Subscription.objects.create(

                shop=shop,

                plan=request.POST.get(
                    'plan'
                ) or 'TRIAL',

                monthly_fee=request.POST.get(
                    'monthly_fee'
                ) or 0,

                payment_status=request.POST.get(
                    'payment_status'
                ) or 'PENDING',

                notes=request.POST.get(
                    'notes'
                ) or ''

            )

        return redirect('/shops/')

    return render(

        request,

        'orders/add_shop.html'

    )
from django.shortcuts import get_object_or_404

from customers.models import Shop, Subscription


@login_required
def edit_shop(request, shop_id):

    if not request.user.is_superuser:

        return redirect('/')

    shop = get_object_or_404(

        Shop,

        id=shop_id

    )

    subscription, created = Subscription.objects.get_or_create(

        shop=shop

    )

    if request.method == 'POST':

        shop.name = request.POST.get(

            'name'

        )

        shop.phone = request.POST.get(

            'phone'

        )

        shop.address = request.POST.get(

            'address'

        )

        shop.default_delivery_days = int(

            request.POST.get(

                'default_delivery_days'

            ) or 2

        )
        shop.is_active = (request.POST.get('is_active') == '1')

        shop.save()


        subscription.plan = request.POST.get(

            'plan'

        )

        subscription.monthly_fee = (

            request.POST.get(

                'monthly_fee'

            ) or 0

        )

        subscription.payment_status = request.POST.get(

            'payment_status'

        )

        subscription.notes = request.POST.get(

            'notes'

        )
        

        subscription.save()

        return redirect('/shops/')


    return render(

        request,

        'orders/edit_shop.html',

        {

            'shop': shop,

            'subscription': subscription

        }

    )
@login_required
def reset_shop_password(

    request,

    shop_id

):

    if not request.user.is_superuser:

        return redirect('/')

    shop = get_object_or_404(

        Shop,

        id=shop_id

    )

    if request.method == 'POST':

        password = request.POST.get(

            'password'

        )

        shop.user.set_password(

            password

        )

        shop.user.save()

        return redirect('/shops/')

    return render(

        request,

        'orders/reset_password.html',

        {

            'shop': shop

        }

    )
@login_required
def deactivate_shop(

    request,

    shop_id

):

    if not request.user.is_superuser:

        return redirect('/')

    shop = get_object_or_404(

        Shop,

        id=shop_id

    )

    shop.is_active = False
    shop.save()

    return redirect('/shops/')
