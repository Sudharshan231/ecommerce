from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>', views.product_detail,name='product_detail'),
    path('add_to_cart/<int:product_id>', views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart_view, name ='cart_view'),
    path('remove-from-cart/<int:cart_itemid>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('order_success',views.order_success,name='order_success'),
    path('register/',views.register_views,name='register_view'),
    path('login/',views.login_view,name='login_view'),
    path('logout',views.logout_view,name='logout_view'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('verify_payment',views.verify_payment,name='verify_payment'),
]

