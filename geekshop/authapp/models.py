from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=0)

    activation_key = models.CharField(
        max_length=128,
        blank=True,
    )

    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

