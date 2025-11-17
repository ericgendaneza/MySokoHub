from django.urls import path
from . import views
urlpatterns = [
    path('',views.Product,name='Product'),
    #path('<int:pk>/',views.product_detail,name='product_detail'),

]



















