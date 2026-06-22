def shop_settings(request):

    if request.user.is_authenticated:

        try:

            return {

                'currency':

                request.user.shop.currency,

                'decimal_places':

                request.user.shop.decimal_places,

            }

        except:

            pass

    return {}

# customers/context_processors.py

from orders.utils import get_current_shop

def current_shop_info(request):

    if request.user.is_authenticated:

        try:

            shop = get_current_shop(request)

            return {

                'currency': shop.currency,

                'decimal_places': shop.decimal_places,

                'current_shop': shop

            }

        except:

            pass

    return {}
