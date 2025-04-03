from django.contrib import admin

from .models import Category, Product, ProductImage, ProductProperties

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductProperties)