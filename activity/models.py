from django.db import models

from django.contrib.auth.models import User

from customers.models import Shop



class ActivityLog(models.Model):

    shop = models.ForeignKey(

        Shop,

        on_delete=models.CASCADE

    )

    user = models.ForeignKey(

        User,

        on_delete=models.SET_NULL,

        null=True

    )

    action = models.CharField(

        max_length=50

    )

    description = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )


    class Meta:

        ordering = ['-created_at']


    def __str__(self):

        return self.action
