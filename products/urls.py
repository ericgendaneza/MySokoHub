from django.urls import path
from . import views
from .views import home
urlpatterns = [
    path('products/', home, name='products'),
    #path('<int:pk>/',views.product_detail,name='product_detail'),

]



















