from django.db import models

# Create your models here.
from shop.models import *

class User(models.Model):
    first_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50, default='whatever')
    mobile_number = models.IntegerField(primary_key=True)
    user_pincode = models.IntegerField()
    user_latitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
    user_longitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
    otp = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + str(self.mobile_number)


class Cart(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return self.user.first_name 
    

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.user.first_name 
    

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return str(self.user.first_name) + str(self.product.product_name)