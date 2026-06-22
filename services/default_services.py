from .models import ServiceCategory, ServiceItem


DEFAULT_SERVICES = {

    'Washing': [

        ('Shirt', 'shirt.png'),
        ('T-Shirt', 'tshirt.png'),
        ('Pants', 'pants.png'),
        ('Jeans', 'jeans.png'),
        ('Dishdasha', 'dishdasha.png'),
        ('Abaya', 'Abaya.png'),
        ('Saree', 'saree.png'),
        ('Salwar', 'salwar.png'),
        ('Jacket', 'jacket.png'),
        ('Coat', 'coat.png'),
        ('Suit', 'suit.png'),
        ('Blanket', 'blanket.png'),
        ('Bedsheet', 'bedsheet.png'),
        ('Curtain', 'curtain.png'),
        ('Pillow Cover', 'pillow.png'),
        ('Carpet', 'carpet.png'),
        ('Shoes', 'shoes.png'),
        ('Bag', 'bag.png'),

    ],

    'Ironing': [

        ('Shirt', 'shirt.png'),
        ('T-Shirt', 'tshirt.png'),
        ('Pants', 'pants.png'),
        ('Jeans', 'jeans.png'),
        ('Dishdasha', 'dishdasha.png'),
        ('Abaya', 'abaya.png'),
        ('Saree', 'saree.png'),
        ('Salwar', 'salwar.png'),
        ('Jacket', 'jacket.png'),
        ('Coat', 'coat.png'),
        ('Suit', 'suit.png'),
        ('Blanket', 'blanket.png'),
        ('Bedsheet', 'bedsheet.png'),
        ('Curtain', 'curtain.png'),

    ],

    'Dry Cleaning': [

        ('Shirt', 'shirt.png'),
        ('Pants', 'pants.png'),
        ('Dishdasha', 'dishdasha.png'),
        ('Abaya', 'abaya.png'),
        ('Suit', 'suit.png'),
        ('Blazer', 'blazer.png'),
        ('Jacket', 'jacket.png'),
        ('Coat', 'coat.png'),
        ('Saree', 'saree.png'),
        ('Salwar', 'salwar.png'),
        ('Wedding Dress', 'dress.png'),
        ('Curtain', 'curtain.png'),
        ('Blanket', 'blanket.png'),

    ],

    'Steam Press': [

        ('Shirt', 'shirt.png'),
        ('Pants', 'pants.png'),
        ('Dishdasha', 'dishdasha.png'),
        ('Abaya', 'abaya.png'),
        ('Suit', 'suit.png'),
        ('Jacket', 'jacket.png'),
        ('Saree', 'saree.png'),

    ],

    'Stain Removal': [

        ('Shirt', 'shirt.png'),
        ('Pants', 'pants.png'),
        ('Dishdasha', 'dishdasha.png'),
        ('Abaya', 'abaya.png'),
        ('Saree', 'saree.png'),
        ('Jacket', 'jacket.png'),
        ('Blanket', 'blanket.png'),
        ('Curtain', 'curtain.png'),

    ],

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
