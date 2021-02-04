from django.db import models
from random import randint
from django.contrib.auth import get_user_model


User = get_user_model()

def create_random_char():
    "Generate a 12 charater long random string"
    char = ''
    chars = 'a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9'.split(' ')
    for i in range(0, 12):
        char += chars[randint(0, len(chars)-1)]
    return char



STATES = (
    "Arizona",
    "Carlifonia",
    "Iowa",
    "Mississippi",
    "Nevada",
    "Ohio",
    "Texas",
)



class Shopper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=70, blank=True, null=True)
    shipping = models.OneToOneField("Shipping", on_delete=models.PROTECT, blank=True, null=True, related_name='ship')
    billing = models.OneToOneField("Billing", on_delete=models.PROTECT, blank=True, null=True, related_name='bill')
    cart = models.OneToOneField("Cart", models.CASCADE, blank=True, null=True, related_name='cart')
    referal_id = models.CharField(max_length=12, blank=True, null=True)
    referals = models.ManyToManyField("Shopper", blank=True, related_name='refs')
    used_coupons = models.ManyToManyField("Discount", blank=True)
    referer_id = models.CharField(max_length=12, blank=True, null=True)
    orders = models.ManyToManyField("Order", blank=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    
    def __str__(self):
        return self.name
    
    
    def get_ref_id(self):
        if not self.referal_id:
            _id = None
            ids = []
            for i in Shopper.objects.all():
                ids.append(i.referal_id)
            while True:
                _id = create_random_char()
                if _id in ids:
                    _id = create_random_char()
                else:
                    self.referal_id = _id
                    break
    
    def get_cart(self):
        if not self.cart:
            from .models import Cart
            cart = Cart(shopper=self)
            cart.save()
            self.cart = cart
            self.save()
            

    @property
    def name(self):
        return self.user.get_full_name()


TAGS = (
    ('hot', "Hot"),
    ('new', "New"),
    ('out', "Sold Out"),
    ('gift', "+free gift"),
)


    
class Item(models.Model):
    name = models.CharField(max_length=70, unique=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    discount = models.DecimalField(decimal_places=2, max_digits=10000, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    tag = models.CharField(max_length=20, default='hot', choices=TAGS)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def like_items(self):
        from django.db.models import Q
        items = Item.objects.all()
        likes = []
        for item in items:
            if item.category in self.category:
                if not item in likes:
                    likes.append(item)
            if item.category == self.category:
                if not item in likes:
                    likes.append(item)
            if item.name in self.name:
                if not item in likes:
                    likes.append(item)
            if item.name == self.name:
                if not item in likes:
                    likes.append(item)
        return likes
    
    
    
    
    
    

class OrderItem(models.Model):
    item = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10000, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.item
    
    def product(self):
        item = Item.objects.get(name=self.item)
        return item
        
    
    @property
    def sub_total(self):
        return self.price * self.quantity
    
    @property
    def image(self):
        img = Item.objects.get(name=self.item)
        return img.image.url
        
    
    
    
    

class Order(models.Model):
    items = models.ManyToManyField("OrderItem", blank=True, related_name='items')
    datetime = models.DateTimeField(auto_now=True)
    failed = models.BooleanField(default=False)
    tracking_id = models.CharField(max_length=12, blank=True, null=True, unique=True)
    discounts = models.ManyToManyField("Discount", blank=True, related_name='coupons')
    amount = models.IntegerField(blank=True, null=True)
    
    def refresh(self):
        for item in self.items.all():
            item.price = item.product().discount if item.product().discount else item.product().price
            item.save()
            
    def transaction(self):
        from api.models import Transaction
        tr = Transaction.objects.get(order=self)
        return tr
        
            
    
    def __str__(self):
        return str(self.tracking_id)
    
    def _set(self):
        if not self.tracking_id:
            id = ''
            ids = []
            for i in Order.objects.all():
                ids.append(i.tracking_id)
            id = create_random_char()
            while True:
                if id in ids:
                    id = create_random_char()
                else:
                    self.tracking_id = id
                    self.save()
                    break
    
    @property
    def invoice(self):
        return self.tracking_id
    
    
    def total(self):
        amt = 0
        for item in self.items.all():
            amt += (item.price * item.quantity)
        if self.discounts:
            for coupon in self.discounts.all():
                amt -= coupon.amount
        self.amount = amt
        self.save()
        return amt
    
    
    def count(self):
        return int(self.items.all().count())
        
    
    
    @property
    def date(self):
        return self.datetime.date()
    
    @property
    def time(self):
        return self.datetime.time()
    
    
class Cart(models.Model):
    shopper = models.ForeignKey("Shopper", models.CASCADE, blank=True, null=True, related_name='owner')
    items = models.ManyToManyField(OrderItem, blank=True)
    
    def total(self):
        amt = 0
        for item in self.items.all():
            amt += item.sub_total
        return amt
    
    def clear(self):
        for item in self.items.all():
            self.items.remove(item)
            item.__reduce__()
        self.save()
    
    @property
    def count(self):
        return self.items.count()

class Billing(models.Model):
    card_holder = models.CharField(max_length=200)
    card_number = models.CharField(max_length=21)
    card_cvv = models.CharField(max_length=3)
    card_exp = models.CharField(max_length=5)
    card_type = models.CharField(max_length=7, default='debit')
    
    def __str__(self):
        return self.card_holder



class Shipping(models.Model):
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=3)
    address = models.TextField()
    postal = models.CharField(max_length=7)
    address2 = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"
    
    
    def __str__(self):
        return '<Shipping Address for %s>' % owner if self.shopper else "Shopper"
    

class Discount(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    code = models.CharField(max_length=15)
    
    
    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
    
    
    def __str__(self):
        return self.code