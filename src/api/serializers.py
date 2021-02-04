from rest_framework import serializers as ser
from .models import (
    Billing_Information,
)


class BillingSerializer(ser.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Billing_Information
