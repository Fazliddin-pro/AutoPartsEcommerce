from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from .managers import CustomUserManager

USER_ROLES = [
    ('admin', 'Administrator'),
    ('seller', 'Seller'),
    ('buyer', 'Buyer'),
]

class CustomUser(AbstractUser):
    """Custom user model replacing the default Django user"""

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Phone Number')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')

    role = models.CharField(max_length=10, choices=USER_ROLES, default='buyer', verbose_name='Role')
    is_verified = models.BooleanField(default=False, verbose_name='Verified User')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return f'{self.email} ({self.role})'


class Address(models.Model):
    """Stores user addresses separately"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100, verbose_name='City')
    street = models.CharField(max_length=255, verbose_name='Street')
    house = models.CharField(max_length=20, verbose_name='House', blank=True, null=True)
    apartment = models.CharField(max_length=20, verbose_name='Apartment', blank=True, null=True)
    postal_code = models.CharField(max_length=10, verbose_name='Postal Code', blank=True, null=True)
    is_default = models.BooleanField(default=False, verbose_name='Default Address')

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house} ({self.user.email})'


class Store(models.Model):
    """Stores seller-specific information"""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=100, verbose_name='Store Name')
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True, verbose_name='Logo')
    description = models.TextField(blank=True, null=True, verbose_name='Store Description')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    
    def clean(self):
        if self.user.role == 'buyer':
            raise ValidationError('A buyer cannot be the owner of a store.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
