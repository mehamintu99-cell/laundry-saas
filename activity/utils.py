from .models import ActivityLog


def log_activity(

    shop,

    user,

    action,

    description

):

    ActivityLog.objects.create(

        shop=shop,

        user=user,

        action=action,

        description=description

    )
