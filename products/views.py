from django.shortcuts import render , redirect
from .models import Product 
from django.contrib import messages
from .forms import ProductForm
from accounts.decorators import vendor_required
from django.core.paginator import Paginator 
from django.shortcuts import render, get_object_or_404



def home(request):
    products=Product.objects.filter(status='active').order_by('-created_at')[:8]
    return render(request, 'SokoHub/home.html', {'products':products})

def product_list(request):
    """
    Task 4.2: Handles product listing, sorting, and pagination.
    """
    products = Product.objects.filter(status='active')


    sort_by = request.GET.get('sort', '-created_at') 
    
    if sort_by == 'price_asc':
        order_by_field = 'price'
    elif sort_by == 'price_desc':
        order_by_field = '-price'
    else: 
        order_by_field = '-created_at' 
        
    products = products.order_by(order_by_field)

    # 
    paginator = Paginator(products, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  
        'sort_by': sort_by     
    }
    
    return render(request, 'products/product_list.html', context)

@vendor_required 
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

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, status='active')
    max_quantity = min(product.stock, 100)
    quantity_range = range(1, max_quantity + 1)

    context = {
        'product': product,
        'quantity_range': quantity_range,
    }
    return render(request, 'products/product_detail.html', context)