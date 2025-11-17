from django.shortcuts import render
from .models import Product 


# Create your views here.
def home(request):
    products=Product.objects.filter(status='active').order_by('-created_at')[:8]
    return render(request, 'products/home.html', {'products':products})


















