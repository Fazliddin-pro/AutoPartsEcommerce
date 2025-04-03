from django.db import models
from users.models import Store
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'parent'], name='unique_category_name_per_parent')
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    stock = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images',
        # validators=[validate_file_size]
        )
    is_main = models.BooleanField(default=False, verbose_name='Is main image')


class ProductProperties(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='properties')
    name =  models.CharField(max_length=255)
    value = models.CharField(max_length=255)