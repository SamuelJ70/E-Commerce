from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up_user'), 
    path('login', views.login, name='login_user'),
    path('index', views.user_index, name='user_index' ),
    path('explore_shop/<str:vendor_number>', views.explore_shop, name='explore_shop'),
    path('add_to_cart/<str:product>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('remove_item/<str:product>', views.remove_item, name='remove_item'),
    path('checkout/<str:product>/<str:quantity>', views.checkout, name='checkout'),
    path('checkouts/', views.checkouts, name="checkouts"),
    path('order', views.order, name='order'),
    path('orders', views.user_orders, name='user_orders'),
    path('user_logout', views.log_out, name='user_logout')
]