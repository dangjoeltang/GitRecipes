from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class UserAccount(AbstractUser):

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user_account = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    short_bio = models.CharField(max_length=400, blank=True)
    profile_photo = models.FileField(upload_to='profile_pics/', blank=True)

    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user_account.username
