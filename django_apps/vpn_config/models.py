from django.db import models
from django.db.models import ForeignKey

from django_apps.users.models import User


class VPNConfig(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Config's ID")
    user = ForeignKey(User, related_name='vpn_configs', on_delete=models.CASCADE)

    objects = models.Manager()

