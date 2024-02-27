from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.User)
admin.site.register(models.Cart)
admin.site.register(models.Checkout)
admin.site.register(models.Orders)