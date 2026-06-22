from customers.models import Shop, Staff


def get_current_shop(request):

    # Owner

    try:

        return request.user.shop

    except:

        pass


    # Staff

    try:

        staff = Staff.objects.get(

            user=request.user

        )

        return staff.shop

    except:

        return None




def get_current_staff(request):

    if request.user.is_superuser:
        return None

    try:
        return Staff.objects.get(
            user=request.user,
            is_active=True
        )
    except Staff.DoesNotExist:
        return None


def is_owner(request):

    if request.user.is_superuser:
        return True

    staff = get_current_staff(request)

    return staff and staff.role == 'OWNER'


def is_staff_user(request):

    staff = get_current_staff(request)

    return staff and staff.role == 'STAFF'
    
