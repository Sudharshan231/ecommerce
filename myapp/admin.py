from django.contrib import admin
from .models import Product, CartItem,Order
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','created_at',]
    search_fields=['name',]
    list_filter = ['created_at']
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity','added_at']
    list_filter = ['added_at']
    search_fields=['user_username','product_name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','name','phone','email','address','total_price','status','order_at']
    list_filter = ['status', 'order_at']
    search_fields=['user_username',]
    filter_horizontal=['items',]