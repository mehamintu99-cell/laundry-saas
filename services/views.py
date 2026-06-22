from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ServiceCategory
from .models import ServiceItem
from orders.utils import get_current_shop

# Create your views here.
@login_required
def category_list(request):

    categories = ServiceCategory.objects.filter(
        shop=get_current_shop(request)
    ).order_by('name')

    if request.method == "POST":

        name = request.POST.get(
            'name',
            ''
        ).strip()

        if not name:

            return render(
                request,
                'orders/categories.html',
                {
                    'categories': categories,
                    'error': 'Category name is required.'
                }
            )

        existing = ServiceCategory.objects.filter(
            shop=get_current_shop(request),
            name__iexact=name
        ).exists()

        if existing:

            return render(
                request,
                'orders/categories.html',
                {
                    'categories': categories,
                    'error': 'Category already exists.'
                }
            )

        ServiceCategory.objects.create(
            shop=get_current_shop(request),
            name=name
        )

        return redirect('/categories/')

    return render(
        request,
        'orders/categories.html',
        {
            'categories': categories
        }
    )
@login_required
def delete_category(request, category_id):

    category = ServiceCategory.objects.get(
        id=category_id,
        shop=get_current_shop(request)
    )

    category.delete()

    return redirect('/categories/')
@login_required
def service_list(request):

    services = ServiceItem.objects.filter(
        shop=get_current_shop(request)
    ).select_related(
        'category'
    ).order_by(
        'category__name',
        'name'
    )

    categories = ServiceCategory.objects.filter(
        shop=get_current_shop(request)
    )

    if request.method == "POST":

        ServiceItem.objects.create(

            shop=get_current_shop(request),

            category_id=request.POST.get(
                'category'
            ),

            name=request.POST.get(
                'name'
            ),

            price=request.POST.get(
                'price'
            ),
            image=request.FILES.get('image')
        )

        return redirect('/services/')

    return render(
        request,
        'orders/services.html',
        {
            'services': services,
            'categories': categories
        }
    )
@login_required
def delete_service(request, service_id):

    service = ServiceItem.objects.get(
        id=service_id,
        shop=get_current_shop(request)
    )

    service.delete()

    return redirect('/services/')
@login_required
def edit_service(request, service_id):

    service = ServiceItem.objects.get(
        id=service_id,
        shop=get_current_shop(request)
    )

    categories = ServiceCategory.objects.filter(
        shop=get_current_shop(request)
    )

    if request.method == "POST":

        price = float(
            request.POST.get('price', 0)
        )

        if price <= 0:

            return render(
                request,
                'orders/edit_service.html',
                {
                    'service': service,
                    'categories': categories,
                    'error': 'Price must be greater than zero.'
                }
            )

        service.name = request.POST.get('name')
        service.price = price
        service.category_id = request.POST.get('category')
        if request.FILES.get('image'):

            service.image = request.FILES.get('image')
    

        service.save()

        return redirect('/services/')

    return render(
        request,
        'orders/edit_service.html',
        {
            'service': service,
            'categories': categories
        }
    )
@login_required
def edit_category(request, category_id):

    category = ServiceCategory.objects.get(
        id=category_id,
        shop=get_current_shop(request)
    )

    if request.method == "POST":

        category.name = request.POST.get(
            "name"
        )

        category.save()

        return redirect('/categories/')

    return render(
        request,
        'orders/edit_category.html',
        {
            'category': category
        }
    )
