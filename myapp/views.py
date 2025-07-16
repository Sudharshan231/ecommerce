from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, CartItem,Order
from.models import User1
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
import razorpay
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
# Create your views here.

@login_required
def product_list(request):
    products=Product.objects.all()
    return render(request,'product_list.html',{'products':products})


def product_detail(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html',{'product':product})


def add_to_cart(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    cart_item, created=CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('cart_view')

def cart_view(request):
    cart_items=CartItem.objects.filter(user=request.user)
    Total_price=sum(item.get_total_price() for item in cart_items)
    return render(request,'cart.html',{'cart_items':cart_items,'total_price':Total_price})

def remove_from_cart(request, cart_itemid):
    cart_item = get_object_or_404(CartItem, id=cart_itemid, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

def checkout(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total_price=sum(item.get_total_price() for item in cart_items)
    total_price_paise=int(total_price* 100)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        

        if not name or not phone or not email or not address:
            return redirect('checkout')
        
        request.session['name'] = name
        request.session['phone'] = phone
        request.session['email'] = email
        request.session['address'] = address
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


        payment=client.order.create({'amount':total_price_paise,
                                    'currency':'INR',
                                    'payment_capture':1})
        # order=Order.objects.create(user=request.user,
        #                             total_price=total_price,
        #                             name=name,
        #                             phone=phone,
        #                             address=address,
        #                             email=email)
        # order.items.set(cart_items)
        # order.save()

        return render(request,'confirm_payment',{'cart_items':cart_items,'total_price':total_price,
                                                    'order_id':payment['id'],
                                                    'razorpay_key':settings.RAZORPAY_KEY_ID,
                                                    'address':address})

    
    return render(request,'checkout.html',{'cart_items':cart_items,'total_price':total_price})
def order_success(request):
    return render(request,'order_success.html')

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        
        name= request.session.get('name')
        phone= request.session.get('phone')
        email= request.session.get('email')
        address= request.session.get('address')

        if razorpay_payment_id and razorpay_order_id:
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.get_total_price() for item in cart_items)


            order=Order.objects.create(user=request.user,
                                    total_price=total_price,
                                    name=name,
                                    phone=phone,
                                    address=address,
                                    email=email,
                                    status='pending')
            order.items.set(cart_items)
            order.save()
            cart_items.delete()

            subject="Order Confirmation message......!!!!!"
            message=f"hii {name},\n\n your order has placed sucessfully.....! Thank you for shopping with us.\n\n Order ID:{order.id}\n Total Amount:{total_price}\n Address:{address}"
            send_mail(subject,message,settings.EMAIL_HOST_USER,[email])

            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'failed'})

        









def register_views(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        User.objects.create_user(username=username,password=password)

        return redirect('login_view')
    return render(request,'register.html')


def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return redirect('product_list')

        else:
            return render(request,'login.html',{'error':'Invalid Login data'})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login/')
