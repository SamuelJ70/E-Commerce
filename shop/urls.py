from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login, name='login'),
    path('otp_verification', views.login, name='otp_verification'),
    path('', views.vendor_home, name='vendor_home'),
    path('vedor_products/', views.vendor_products, name='vendor_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<str:product>', views.edit_product, name='edit_product'),
    path('logout', views.log_out, name='log_out'),
    path('vendor_profile', views.profile, name='vendor_profile'),
    path('shop_orders', views.shop_orders, name='shop_orders')
 
]

