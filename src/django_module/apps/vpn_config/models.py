from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import ForeignKey

from django_module.apps.users.models import User


class VPNConfig(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Config's ID")
    user = ForeignKey(User, related_name='vpn_configs', on_delete=models.CASCADE)
    # "Interface"
    private_key = models.CharField(max_length=64)
    address = models.CharField(max_length=50)
    # "Peer"
    public_key = models.CharField(max_length=64)
    allowed_ips = ArrayField(models.CharField(max_length=50))  # Storing allowed IPs as an array
    endpoint = models.CharField(max_length=100)

    persistent_keepalive = models.PositiveIntegerField()

    objects = models.Manager()


