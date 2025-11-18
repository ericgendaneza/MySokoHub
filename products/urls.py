from django.urls import path
from . import views
from .views import home
from .views import add_product
urlpatterns = [
    path('products/', home, name='products'),
    #path('<int:pk>/',views.product_detail,name='product_detail'),

]

urlpatterns += [
    path('add_product/', add_product, name='add_product'),
]

















