from django.shortcuts import redirect
from django.contrib import messages

from customers.models import Staff


def owner_required(view_func):

    def wrapper(request, *args, **kwargs):

        # Super Admin

        if request.user.is_superuser:

            return view_func(
                request,
                *args,
                **kwargs
            )

        # Owner

        try:

            staff = Staff.objects.get(

                user=request.user,

                is_active=True

            )

            if staff.role == 'OWNER':

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

        except Staff.DoesNotExist:

            pass

        messages.error(

            request,

            "You do not have permission."

        )

        return redirect('/')


    return wrapper
