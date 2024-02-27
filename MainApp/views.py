from django.shortcuts import render, redirect

# Create your views here.


from django.http import HttpResponse
from random import random
import os
from twilio.rest import Client
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect


from .models import *
from shop.models import *

def index(request):
   
    return render(request, 'index/index.html')


def sign_up(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        
        pincode = request.POST['pincode']
        
        
        if len(password) < 8:
            messages.info(request, "Password lenght shouldn't be less than 8")
            return render(request, 'users/sign_up.html')
        
        if len(mobile_number) < 10 or len(mobile_number) > 10:
            messages.info(request, "Phone number can't be less than 10 or greater than 10 numbers")
            return render(request, 'users/sign_up.html')
        
        if mobile_number[0] not in ['6', '7', '8', '9']:
            messages.info(request, "The phone number entered is not a valid number")
            return render(request, 'users/sign_up.html')
        
    
        user_obj = User.objects.filter(mobile_number = mobile_number)
        print(user_obj)

        if user_obj.exists():
            messages.info(request, "Your account already exists please login")
            return redirect('login_user')
        
        else:   #create user object if the user is not found

          
            #creating shop object if the vendor is not found
            otp = int((random() * 10000))
            try:          
                

                #using twilio to send otp
                account_sid = "AC142f7c9db5bab981d910d9e99e9d2049"
                auth_token = "375bde512bfbdfa7c70b7bcda795c8f1"
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                body=f"Your Direct store OTP is {otp}", from_="+18148015571", to="+91" + request.POST['mobile_number'])
                #end of twilio block

                #user object is created and saved

                user_obj = User(first_name = first_name, mobile_number = mobile_number, password = password, user_pincode = pincode, otp = otp)
                
                user_obj.save()
                
                messages.info(request, "Please login with the otp sent to your phone number")
                return redirect('login_user')
            except:
                user_obj = User(first_name = first_name, mobile_number = mobile_number, password = password, user_pincode = pincode, otp = otp)
                user_obj.is_verified = True
                user_obj.save()
                messages.info(request, "Please login with the password")
                return redirect('login_user') 

    return render(request, 'users/sign_up.html' )



def login(request):

    if request.method == 'POST':
        
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']

        print(mobile_number,password)
        try:
            user_obj = User.objects.get(mobile_number = mobile_number)
            
        except:
            messages.info(request, "Phone number doesn't exist please sign up")
            return render(request, 'users/sign_up.html')
      
        
        if not user_obj.is_verified:
            if (str(user_obj.otp) == str(password)):
                user_obj.is_verified = True
                user_obj.save()
                request.session['user'] = user_obj.mobile_number
                return redirect('user_index')
            else:
                messages.info(request, "You entered wrong otp")
                return redirect('login_user')
        
        if user_obj:
            if (user_obj.password == password):
                request.session['user'] = user_obj.mobile_number
                return redirect('user_index')
            else:
                messages.info(request, "You entered wrong password")
                return redirect('login_user')
            

    return render(request, 'users/login.html')


def user_index(request):
    
    request.session['vendor'] = None

    user_obj = User.objects.get(mobile_number = request.session['user'])
    shop_qs = Vendor.objects.filter(pincode = user_obj.user_pincode)
    
    

    return render(request, 'users/index.html', context={'shops' : shop_qs})


def explore_shop(request, vendor_number):
    
    shop = Vendor.objects.get(mobile_number = vendor_number)
    shop_products = Product.objects.filter(shop = shop)
    print(shop_products)

    context = {
        'shop_products' : shop_products
    }

    request.session['vendor'] = vendor_number
    print(request.session['vendor'])
    return render(request, 'users/shop_explore.html', context=context)


def add_to_cart(request, product):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    print(user_obj)
    product_obj = Product.objects.get(product_name = product)


    #checking if the item is already present in the cart
    items = Cart.objects.filter(user = user_obj, product = product_obj)

    if items.exists():
        messages.info(request, "Item already in the cart")
        url = reverse('explore_shop', args=[request.session['vendor']])
        return redirect(url)
    
    
    cart = Cart(user = user_obj, product = product_obj)
    cart.save()

    messages.info(request, "Sucessfully added to cart ")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    cart = Cart.objects.filter(user = user_obj)
    print(cart)

    return render(request, 'users/cart.html', context={'cart' : cart})


def remove_item(request, product):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    item = Cart.objects.get(user = user_obj, product= product)
    item.delete()

    messages.info(request, "Item removed Successfully")
    return redirect('cart')

def checkout(request, product, quantity):
    
    product_obj = Product.objects.get(product_name = product)
    user_obj = User.objects.get(mobile_number = request.session['user'])
    
    

    quantity = int(quantity.strip())
    
    #check if the product already in the checkout if so add to the existing product itself
    existing_product = Checkout.objects.filter(user = user_obj, product = product_obj)

    if existing_product :
        existing_product[0].quantity += quantity
        existing_product[0].save()
        return redirect('cart')

    print(quantity)
    checkout_obj = Checkout(user = user_obj, product = product_obj, quantity = quantity)

    checkout_obj.save()

    cart_obj = Cart.objects.filter(user = user_obj, product = product_obj)
    cart_obj.delete()

    messages.info(request, "Product added to checkout successfully")

    return redirect('cart')

def checkouts(request):

    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    print(user_obj)
    
    
    checkout_obj = Checkout.objects.filter(user = user_obj)
    print(checkout_obj)
    return render(request, 'users/checkout.html', context={'products' : checkout_obj})


def order(request):
    
    #in order to do order view we are taking data from checkout
    user_obj = User.objects.get(mobile_number = request.session['user'])
    checkout_obj = Checkout.objects.filter(user = user_obj)

    for product in checkout_obj:
        # print(product.product.shop, type(product.product.shop))
        # print(product.product, type(product.product))
        # print(product.quantity)
        order_obj = Orders(user = user_obj, shop = product.product.shop, product=product.product, quantity = product.quantity ) 
        
        #Reducing the quantity of the product

        ordered_quantity = product.quantity
        acutal_quantity = product.product.product_quantity

        new_quantity = acutal_quantity - ordered_quantity

        product_obj = product.product

        product_obj.product_quantity = new_quantity

        product_obj.save()

        product.delete()

        order_obj.save()

    messages.info(request, "Ordered placed successfully")
    return redirect('user_orders')


def user_orders(request):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    order_obj = Orders.objects.filter(user = user_obj)

    return render(request, 'users/orders.html', context={'products' : order_obj})

def log_out(request):

    request.session['user'] = ''
    return redirect('/')