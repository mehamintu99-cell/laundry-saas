from django.shortcuts import redirect
from django.contrib import messages

from .utils import is_owner


def owner_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:

            return view_func(
                request,
                *args,
                **kwargs
            )

        if is_owner(request):

            return view_func(
                request,
                *args,
                **kwargs
            )

        messages.error(
            request,
            "You do not have permission."
        )

        return redirect('/')

    return wrapper
