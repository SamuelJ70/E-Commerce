from django.db import models

# Create your models here.
from django.urls import reverse

class Vendor(models.Model):
    shop_name = models.TextField(max_length=50)
    mobile_number = models.CharField(max_length=10, primary_key=True)
    password = models.TextField(max_length=50)
    pincode = models.IntegerField()
    otp = models.IntegerField(null=True, default=None, blank=True)
    is_verified = models.BooleanField(default=False)
    shop_image = models.ImageField(upload_to="shops/", null=True, blank=True)

    def __str__(self) -> str:
        return self.shop_name



class ProductCategory(models.Model):
    category = models.TextField(max_length=50)

    def __str__(self) -> str:
        return self.category
    
class Product(models.Model):
    product_name = models.TextField(max_length=50, primary_key=True)
    product_price = models.IntegerField()
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    product_details = models.TextField(max_length=100)
    product_image = models.ImageField(upload_to="products/")
    shop = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=0)

    def get_absolute_url(self):
        return self.product_name


    def __str__(self) -> str:
        return self.product_name


