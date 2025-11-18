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
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.status = 'active'
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})
















