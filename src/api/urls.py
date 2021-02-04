from django.urls import path
from .views import (
    BillingListView,
    BillingDetailView
)



app_name = 'api'


urlpatterns = [
    path('clients/', BillingListView.as_view(), name='clients-list'),
    path('clients/<pk>/', BillingDetailView.as_view(), name='client-detail')
]
