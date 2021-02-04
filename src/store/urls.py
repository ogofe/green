from django.urls import path, re_path
from django.contrib.auth import logout
from .views import (
    store_view,
    product_detail_view,
    cart_view,
    add_to_cart,
    add_one_to_cart,
    remove_from_cart,
    increase_cart_item, 
    decrease_cart_item,
    checkout_view,
    redeem_discount,
    signup_view,
    signin_view,
    signout,
    start_checkout,
    pay,
    error,
    orders_view,
    delete_order,
)


app_name = "Store"



urlpatterns = [
    path('', store_view, name='store'),
    path('item/<int:item_id>/details', product_detail_view, name='item-detail'),
    path('cart/', cart_view, name='cart'),
    path('orders/', store_view, name='orders'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/<invoice>/', checkout_view, name='checkout'),
    path('<transaction_id>/pay/', pay, name='pay'),
    path('signup/', signup_view, name='register'),
    path('signin/', signin_view, name='login'),
    path('signout/', signout, name='logout'),
    path('my-orders', orders_view, name="orders"),
    
    # methods
    
    # item
    path('cart/<item>/add-to/cart/', add_one_to_cart, name='add-one-to-cart'),
    path('cart/<item>/plus/', add_to_cart, name='add-to-cart'),
    # cart item
    path('cart/<item>/remove-from/cart/', remove_from_cart, name='remove-from-cart'),
    path('cart/<item>/increase/', increase_cart_item, name='increase-cart-item'),
    path('cart/<item>/decrease/', decrease_cart_item, name='decrease-cart-item'),
    # checkout 
    path('checkout/<invoice>/redeem/', redeem_discount, name='redeem'),
    path('pay/start/', start_checkout, name='start-pay'),
    path('pay/complete/', error, name='error'),
    # order
    path('my-orders/delete/<order_id>/', delete_order, name="del-order"),
]
