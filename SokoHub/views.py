from django.shortcuts import render
from products.models import Product

def home(request):  
    try:
        newest_products = Product.objects.filter(status='active').order_by('-created_at')[:8]
    except Exception as e:
        print(f"Error fetching newest products: {e}")
        newest_products = []
        context = {'newest_products': newest_products}
        return render(request, 'SokoHub/home.html', context)
    def product_list(request):
        all_products = Product.objects.filter(status='active').order_by('name')

        context = {'all_products': all_products}
        return render(request, 'products/home.html', context)
