from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid


ROLES = (
    ('Customer', 'Customer'),
    ('Editor', 'Editor'),
    ('Admin', 'Admin'),
)

class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserData(AbstractUser):
    role = models.CharField(choices=ROLES, default=ROLES[0], max_length=32)
    username = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    address = models.CharField(max_length=128, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nonce_expired = models.BooleanField(default=True)
    public_seed = models.CharField(max_length=36, default=uuid.uuid4)
    private_seed = models.CharField(max_length=36, default=uuid.uuid4)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.email} {self.address} {self.first_name} {self.last_name}'


class NonceSignRequest(models.Model):
    address = models.CharField(max_length=128, blank=False)
    nonce = models.CharField(max_length=128, default=uuid.uuid4, unique=True)
    user = models.ForeignKey('authentication.UserData', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('address', 'nonce')

    def save(self, *args, **kwargs):
        super(NonceSignRequest, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.address} {self.nonce} {self.user}'
