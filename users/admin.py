from django.contrib import admin
from .models import CustomUser, Address, Store

admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(Store)
