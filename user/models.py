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

    @property
    def username(self):
        return self.user_account.username

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    short_bio = models.CharField(max_length=400, blank=True)
    profile_photo = models.CharField(
        max_length=400, blank=True, default='profile-photos/profile-pic-placeholder_500x500.png')

    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user_account.username
