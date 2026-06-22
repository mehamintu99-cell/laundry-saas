from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .models import ActivityLog

from orders.utils import get_current_shop

from customers.decorators import owner_required
from customers.models import Staff


@login_required

@owner_required

def activity_list(request):

    activities = ActivityLog.objects.filter(

        shop=get_current_shop(request)

    ).select_related(

        'user'

    )
    for activity in activities:

        activity.display_name = activity.user.username

        activity.display_role = ''

        if activity.user.is_superuser:

            activity.display_role = 'SUPER ADMIN'

        else:

            try:

                staff = Staff.objects.get(user=activity.user)

                activity.display_name = staff.full_name

                activity.display_role = staff.role

            except Staff.DoesNotExist:

                pass

    return render(

        request,

        'activity/activity_list.html',

        {

            'activities': activities

        }

    )
