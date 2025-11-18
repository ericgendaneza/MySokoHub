# orders/urls.py
from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('vendor-orders/', views.vendor_orders, name='vendor_orders'),
    path('vendor-orders/<int:order_id>/', views.vendor_order_details, name='vendor_order_details'),

]
