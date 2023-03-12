from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, is_active=True, is_staff=False, password=None):
        # if not password:
        #     raise ValueError('password is required')
        if not username:
            raise ValueError('username is required')

        user: User = self.model(username=username)
        user.password = make_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.save(using=self.db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username)
        user.password = make_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'User'


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    avatar = models.ImageField(upload_to='images/', verbose_name=_('avatar'), default='images/Default.jpg')
    point = models.PositiveIntegerField(verbose_name=_('point'), default=0)
    coin = models.PositiveIntegerField(verbose_name=_('coin'), default=0)

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin', verbose_name=_('user'))

    def __str__(self):
        return self.user.username
