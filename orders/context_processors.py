from customers.models import Staff


def staff_info(request):

    staff = None

    if request.user.is_authenticated:

        try:

            staff = Staff.objects.get(

                user=request.user,

                is_active=True

            )

        except Staff.DoesNotExist:

            pass

    return {

        'current_staff': staff

    }
