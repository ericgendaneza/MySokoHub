from django.urls import path
from . import views
# from .views import home
# from .views import add_product

urlpatterns = [
    # path('products/', home, name='products'),
    path('', views.home, name = 'home_page'),
    path('products/', views.product_list, name='product_list'),
    path('<int:pk>/',views.product_detail,name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]

# urlpatterns += [
#     path('add_product/', add_product, name='add_product'),
# ]

















