from django.contrib import admin
from .models import (
    Shipping,
    Shopper,
    Discount,
    Cart,
    OrderItem,
    Order,
    Billing,
    Item
)


admin.site.register(Shipping)
admin.site.register(Shopper)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Billing)
admin.site.register(Item)