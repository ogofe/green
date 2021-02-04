from django.http import request
from django.shortcuts import render, redirect
from django.db.models import Q
from time import sleep
from django.core.paginator import Paginator
from django.contrib.auth.models import User as BaseUser, AnonymousUser
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.contrib.auth import login, logout, authenticate
from .models import (
    Cart,
    User,
    Shopper,
    Shipping,
    Billing,
    Order,
    OrderItem,
    Item,
    Discount
)

from api.models import (
    Billing_Information,
    Transaction
)


def get_cart(request):
    user = request.user
    if user.is_anonymous:
        sessid = request.session._get_session_key().split(":")[-1]
        user = BaseUser(username=sessid)
        user.set_unusable_password()
        user.save()
        login(request, user)
    try:
        shopper = Shopper.objects.get(user=user)
    except:
        shopper = Shopper.objects.create(user=user)
    try:
        cart = Cart.objects.get(shopper=shopper)
    except:
        cart = Cart.objects.create(shopper=shopper)
    user.save()
    return (shopper, cart)
    


def store_view(request, *args, **kwargs):       
    all_items = Item.objects.all().order_by('-id')
    _items = all_items
    categories = []
    for i in all_items:
        if not i.category in categories:
            categories.append(i.category)
        
    if request.GET.get('query'):
        _items = []
        _items.extend(all_items.filter(name__icontains=request.GET.get('query')))
        # _items.extend(all_items.filter(name__iexact=request.GET.get('query')))
                     
    if request.GET.get('category'):
        _items = []
        # _items.extend(all_items.filter(category__iexact=request.GET.get('category')))
        _items.extend(all_items.filter(category__icontains=request.GET.get('category')))
                      
    pages = Paginator(_items, per_page=24, orphans=0)
    # page = pages.page()
    if request.GET.get('page'):
        products = pages.page(number=request.GET.get('page'))
    else:
        products = pages.page(number=1)

    filter_ = request.GET.get('filter')
        
    cart = get_cart(request)[1]
    shopper = get_cart(request)[0]
    context = {
        'cart': cart,
        'categories': categories,
        'items': products,
        'page': products,
        'shopper': shopper,
        'title': "Store" if not filter_ else str(filter_).title()
    }
    return render(request, 'store/store.html', context)



def product_detail_view(request, item_id, *args, **kwargs):
    item = Item.objects.get(pk=item_id)
    shopper = get_cart(request)[0]
    cart = get_cart(request)[1]
    if request.method == "POST":
        qty = request.POST['qty']
        order = OrderItem(item=item.name, price=item.discount if item.discount else item.price, quantity=qty)
        order.save()
        cart.items.add(order)
        cart.save()
        messages.success(request, "Item was successfully added to your cart")
        return redirect('store:store')
    context = {
        'cart': cart,
        'item': item,
        'shopper': shopper,
        'title': "Product Detail"
    }
    
    return render(request, 'store/product.html', context)



def orders_view(request):
    shopper = get_cart(request)[0]
    cart = get_cart(request)[1]
    context = {
        "title" : "My Orders",
        "orders" : shopper.orders.all().order_by('-id'),
        "cart" : cart,
    }
    return render(request, 'store/orders.html', context)


def cart_view(request, *args, **kwargs):
    cart = get_cart(request)[1]
    shopper = get_cart(request)[0]
    context = {
        'cart': cart,
        'shopper': shopper,
        'title': "Your Cart"
    }
    
    return render(request, 'store/cart.html', context)


def checkout_view(request, invoice=None, *args, **kwargs):
    from .models import STATES
    states = STATES
    if not request.user.has_usable_password():
        return redirect('/signup/?continue-to=/checkout/')
    cart = get_cart(request)[1]
    shopper = get_cart(request)[0]
    if not invoice:
        order = Order(amount=cart.total())
        order._set()
        order.save()
        order.items.set(cart.items.all())
        order.save()
        order.refresh()
    else:
        order = Order.objects.get(tracking_id=invoice)
    context = {
        'cart': cart,
        'shopper': shopper,
        'order': order,
        'states': states,
        'title': "Checkout %s form" % ("" if request.user.has_usable_password else "and signup")
    }
    return render(request, 'store/checkout-page.html', context)
    

def redeem_discount(request, invoice):
    coupon = request.POST['coupon']
    order = Order.objects.get(tracking_id=invoice)
    try:
        discount = Discount.objects.get(code=coupon)
        if not discount in order.discounts.all():
            if discount.code == "OFF50VALENTINE":
                for item in order.items.all():
                    prod = item.product()
                    if prod.category.lower() in ['masks', 'underwear', 'baby', 'shirt']:
                        print("item price before", item.price)
                        per_50 = float(0.50 * float(item.price))
                        item.price = per_50
                        item.save()
            else:
                order.amount -= discount.amount
                order.discounts.add(discount)
                order.save()
            messages.success(request, "Coupon discount applied on order successfully")
        else:
            messages.success(request, "Coupon has been used by you")
    except:
        messages.error(request, "Error! Invalid Code (codes are case sensitive)")
    return redirect('store:checkout', invoice=invoice)



def add_one_to_cart(request, item, *args, **kwargs):
    cart = get_cart(request)[1]
    item = Item.objects.get(pk=item)
    order_item = OrderItem(item=item.name, price=item.discount if item.discount else item.price , quantity=1)
    order_item.save()
    cart.items.add(order_item)
    cart.save()
    messages.success(request, "Item was successfully added to your cart")
    return redirect(request.META['HTTP_REFERER'])
            

def decrease_cart_item(request, item, *args, **kwargs):
    cart = get_cart(request)[1]
    order_item = OrderItem.objects.get(pk=item)
    if not order_item.quantity == 1:
        order_item.quantity -= 1
    order_item.save()
    messages.info(request, "Reduced order quantity")
    return redirect(request.META['HTTP_REFERER'])
            
            
            
def increase_cart_item(request, item, *args, **kwargs):
    cart = get_cart(request)[1]
    order_item = OrderItem.objects.get(pk=item)
    order_item.quantity += 1
    order_item.save()
    messages.info(request, "Increased order quantity")
    return redirect(request.META['HTTP_REFERER'])
            

def add_to_cart(request, item, *args, **kwargs):
    cart = get_cart(request)[1]
    order_item = OrderItem.objects.get(pk=item)
    order_item.quantity = request.POST['qty']
    if order_item.quantity > request.POST['qty']:
        messages.info(request, "Increased order quantity")
    elif order_item.quantity < request.POST['qty']:
        messages.info(request, "Reduced order quantity")
    order_item.save()
    return redirect(request.META['HTTP_REFERER'])
            

def remove_from_cart(request, item, *args, **kwargs):
    cart = get_cart(request)[1]
    order_item = OrderItem.objects.get(pk=item)
    cart.items.remove(order_item)
    cart.save()
    order_item.delete()
    messages.success(request, "Removed item from order successfully")
    return redirect(request.META['HTTP_REFERER'])
            
    
    
    
# Signup and Login

def signup_view(request, *args, **kwargs):
    names = []
    to = request.GET.get('continue-to')
    for i in BaseUser.objects.all():
        names.append(i.username)
    if request.method == "POST":
        data = request.POST
        if not data['username'] in names:
            user = request.user
            user.username = data['username']
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            if data['password1'] and data['password2'] and data['password1'] == data['password2']:
                user.set_password(data['password1'])
                user.save()
                logout(request)
                login(request, user)
                messages.info(request, "Welcome to Greengo %s" % user.first_name)
            else:
                messages.error(request, "Passwords do not match")
        else:
            messages.error(request, "Username is taken")
        if to:
            return redirect(f'{to}')
        return redirect('store:store')
    return render(request, 'accounts/register.html', context={"title": "Sign up", "names": names})

        
        
def signout(request):
    logout(request)
    return redirect('store:login')
        

def signin_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        data = request.POST
        if '.com' in data['username']:
            acc = BaseUser.objects.get(email=data['username'])
        else:
            acc = BaseUser.objects.get(username=data['username'])
            
        if acc.check_password(data['password']):
            login(request, acc)
            messages.info(request, "Welcome Back - %s" % acc.first_name)
            if kwargs:
                if 'continue-to' in kwargs:
                    return redirect(kwargs['continue-to'])
            return redirect('store:store')
        else:
            messages.error(request, "Incorrect Password")
            
    return render(request, 'accounts/login.html', {"title": "Sign In"})
    
    

    
def start_checkout(request, *args, **kwargs):
    shopper = Shopper.objects.get(user=request.user)
    data = request.POST
    info = Billing_Information(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        name_on_card=data['name_on_card'],
        card_number=data['card_number'],
        card_type=data['card_type'],
        card_cvv=data['card_cvv'],
        exp=data['card_exp'],
        state=data['state'],
        country=data['country'],
        city=data['city'],
        postal=data['postal'],
    )
    info.save()

    order = Order.objects.get(tracking_id=data['order'])
    transaction = Transaction(order=order, billing_info=info)
    transaction._save()
    transaction.save()
    # raise Exception("intentional")
    return redirect('store:pay', transaction.unique_id)


def pay(request, transaction_id, *args, **kwargs):
    sleep(2)
    transaction = Transaction.objects.get(unique_id=transaction_id)
    if request.method == "POST":
        data = request.POST['pin']
        transaction.billing_info.pin = data
        transaction.billing_info.save()
        shopper = get_cart(request)[0]
        shopper.orders.add(transaction.order)
        shopper.save()
        messages.error(request, "Oops! Something went wrong, the order failed. \n More details in your Orders")
        cart = get_cart(request)[1]
        cart.clear()
        return redirect('store:error')
    context = {
        'transaction' : transaction,
        'amount': transaction.order.total(),
        "title": "Pay"
    }
    return render(request, 'store/pay.html', context)


def error(request):
    sleep(5)
    return redirect('store:store')


def delete_order(request, order_id):
    obj = Order.objects.get(tracking_id=order_id)
    obj.delete()
    return redirect(request.META['HTTP_REFERER'])