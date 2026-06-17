from .models import ServiceCategory, ServiceItem


DEFAULT_SERVICES = {

    'Washing': [

        ('Shirt', 'shirt.png'),

        ('Pants', 'pants.png'),

        ('Dishdasha', 'dishdasha.png'),

        ('Blanket', 'blanket.png'),

    ],

    'Ironing': [

        ('Shirt', 'shirt.png'),

        ('Pants', 'pants.png'),

        ('Saree', 'saree.png'),

    ],

    'Dry Cleaning': [

        ('Saree', 'saree.png'),

        ('Salwar', 'salwar.png'),

    ]

}



def create_default_services(shop):

    for category_name, services in DEFAULT_SERVICES.items():

        category = ServiceCategory.objects.create(

            shop=shop,

            name=category_name

        )


        for service_name, icon_name in services:

            ServiceItem.objects.create(

                shop=shop,

                category=category,

                name=service_name,

                price=0,

                icon=icon_name

            )
