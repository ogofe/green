from django.shortcuts import render
from rest_framework.viewsets import generics as gen, mixins
from .serializers import BillingSerializer
from .models import Billing_Information
from rest_framework.permissions import BasePermission   


class IsAdminOrNot(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_staff == True:
            return True
        return False
    
        

class BillingListView(gen.ListAPIView):
    # permission_classes = [IsAdminOrNot]
    serializer_class = BillingSerializer
    queryset = Billing_Information.objects.all().order_by('-id')
    
    


class BillingDetailView(gen.RetrieveAPIView):
    # permission_classes = [IsAdminOrNot]
    serializer_class = BillingSerializer
    queryset = Billing_Information.objects.all().order_by('-id')
    lookup_field = 'pk'
    
    

