# Add app_name to allow namespacing from project urls
from django.urls import path
from . import views

app_name = 'products'
# from .views import home
# from .views import add_product

urlpatterns = [
    # path('products/', home, name='products'),
    path('', views.home, name = 'home_page'),
    path('products/', views.product_list, name='product_list'),
    path('<int:pk>/',views.product_detail,name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/products/', views.vendor_products, name='vendor_products'),
    path('vendor/products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('vendor/products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    
    # Cart URLs

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

]

# urlpatterns += [
#     path('add_product/', add_product, name='add_product'),
# ]

















