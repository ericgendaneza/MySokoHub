from django.shortcuts import render , redirect
from .models import Product, Cart
from django.contrib import messages
from .forms import ProductForm
from accounts.decorators import vendor_required
from django.core.paginator import Paginator 
from django.shortcuts import render, get_object_or_404
from orders.models import OrderItem
from django.db.models import Sum, Q, Count
from django.contrib.auth.decorators import login_required



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
            return redirect('products:vendor_dashboard')
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


@vendor_required
def vendor_dashboard(request):
    vendor = request.user
    total_products = Product.objects.filter(vendor=vendor).count()
    active_products = Product.objects.filter(vendor=vendor, status='active').count()
    out_of_stock = Product.objects.filter(vendor=vendor, stock=0).count()

    # Count order items related to this vendor's products
    pending_order_items = OrderItem.objects.filter(product__vendor=vendor, order__status='pending').count()

    recent_products = Product.objects.filter(vendor=vendor).order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'pending_order_items': pending_order_items,
        'recent_products': recent_products,
    }
    return render(request, 'products/vendor_dashboard.html', context)


@vendor_required
def vendor_products(request):
    vendor = request.user
    products = Product.objects.filter(vendor=vendor).order_by('-created_at')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/vendor_products.html', {'page_obj': page_obj})


@vendor_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products:vendor_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@vendor_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products:vendor_products')
    return render(request, 'products/confirm_delete.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='active')
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        messages.error(request, 'Invalid quantity selected.')
        return redirect('products:product_detail', pk=product_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f'Added {quantity} of {product.name} to your cart.')
    return redirect('products:product_detail', pk=product_id)

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('products:view_cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('products:view_cart')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        # Here you would typically create an Order and OrderItems
        cart_items.delete()
        messages.success(request, 'Checkout successful! Your order has been placed.')
        return redirect('SokoHub:home_page')
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)   