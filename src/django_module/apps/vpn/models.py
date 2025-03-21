from __future__ import annotations

from typing import Union, Optional, Tuple

from django.db import models
from django.db.models import Manager
from telegram import Update
from telegram.ext import CallbackContext

from django_module.apps.utils.models import CreateUpdateTracker


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class Client(CreateUpdateTracker):
    username = models.TextField(max_length=50, blank=True, null=True)
    chat_id = models.BigIntegerField(
        blank=True, null=True, help_text='Unique identifier for the chat with the user', unique=True,
    )
    is_admin = models.BooleanField(default=False)

    admins = AdminUserManager()  # User.admins.all()
    objects = models.Manager()

    def __str__(self):
        return f'username: @{self.username}' if self.username is not None else f'id: {self.id}'

    @classmethod
    async def get_client_or_create(cls, update: Update, context: CallbackContext) -> Tuple[Client, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        user_dict_data = update.effective_user.to_dict()
        u, created = await cls.objects.aget_or_create(
            chat_id=user_dict_data["id"],
            username=user_dict_data['username']
        )

        return u, created

    @classmethod
    def get_client_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[Client]:
        """Search user in DB, return User or None if not found."""
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    async def get_admin_clients(cls):
        return await cls.objects.filter(is_admin=True).all()


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    start_date = models.DateField(null=False, blank=False, verbose_name='Start date')
    end_date = models.DateField(null=False, blank=False, verbose_name='End date')
    amount = models.IntegerField(null=False, blank=False, verbose_name='Price for subscription')

    def __str__(self):
        return (
            f'client: @{self.client.id}, config: {self.config.id}, '
            f'start_date: {self.start_date}, end_date: {self.end_date}, amount: {self.amount}',
        )


class Config(models.Model):
    data = models.JSONField(default=dict, verbose_name='Config data')
    activated = models.BooleanField(null=False, blank=False, verbose_name='Is active config')
    vpn_id = models.IntegerField(null=False, blank=False, verbose_name='Id in vpn service')
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)


class PaymentHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    payment_time = models.DateTimeField(null=False, blank=False, verbose_name='Payment date')
    transaction_id = models.TextField(null=False, blank=False, verbose_name='Transaction ID')
    amount = models.IntegerField(null=False, blank=False, verbose_name='Amount in Telegram starts')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)

