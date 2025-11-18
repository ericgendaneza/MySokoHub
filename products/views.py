from django.shortcuts import render , redirect
from .models import Product 
from django.contrib import messages
from .forms import ProductForm
from accounts.decorators import vendor_required

# Create your views here.
def home(request):
    products=Product.objects.filter(status='active').order_by('-created_at')[:8]
    return render(request, 'products/home.html', {'products':products})

def add_product(request):
    if request.method == 'POST':
       product_name=request.POST.get('name')
       product_price=request.POST.get('price')
       product_description=request.POST.get('description')
       product_image=request.POST.get('image')
       product_stock=request.POST.get('stock')

       product=Product.objects.create( 
        name=product_name,
        price=product_price,
        description=product_description,
        image=product_image,
        stock=product_stock,
        vendor=request.user
       )
       product.save()
       messages.success(request, 'Product added successfully')
       return redirect('home')
    return render(request, 'products/add_product.html')
    
    













