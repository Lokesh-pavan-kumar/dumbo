from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class DumboUserManager(BaseUserManager):
    def create_user(self, email, username, fullname, password=None, **kwargs):
        if not email:
            raise ValueError('All users must have a unique email')
        if not username:
            raise ValueError('All users must have a unique username')
        if not fullname:
            raise ValueError('Users must have a fullname')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fullname, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs['is_staff'] is False:
            raise ValueError('is_staff must be set to True for Superusers')
        if kwargs['is_superuser'] is False:
            raise ValueError('is_superuser must be set to True for Superusers')
        return self.create_user(email, username, fullname, password, **kwargs)


class DumboUser(AbstractBaseUser):
    # Fields that are specific for our users
    email = models.EmailField(unique=True, verbose_name='Email Id')
    username = models.CharField(max_length=100, unique=True, verbose_name='Username')
    fullname = models.CharField(max_length=255, verbose_name='Fullname')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Date Joined')
    phone_number = models.CharField(max_length=12, verbose_name='Phone number')

    # Fields that are required by django to provide permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = DumboUserManager()

    REQUIRED_FIELDS = ['fullname', 'email']
    USERNAME_FIELD = 'username'  # We will be using the username to identify the users
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission?
        # Always true!
        return True

    def has_module_perms(self, app_label):
        # Does the user have permission to view a particular app?
        # Always true
        return True
