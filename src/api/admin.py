from django.contrib import admin
from .models import (
    Transaction,
    Billing_Information
)



admin.site.register(Transaction)
admin.site.register(Billing_Information)