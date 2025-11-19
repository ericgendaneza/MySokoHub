# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CheckoutForm
from .models import Order, OrderItem
from products.models import Product
from django.http import JsonResponse
from django.shortcuts import reverse

@login_required
def checkout(request, product_id):
    # Only customers should be allowed to place orders
    if getattr(request.user, 'user_type', None) != 'customer':
        messages.error(request, "Only customers can place orders. Please log in as a customer.")
        return redirect('products:product_list')  # adjust to your product list url name

    product = get_object_or_404(Product, id=product_id)

    # Prevent checkout if product out of stock
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('products:product_detail', pk=product.id)  # adjust as needed

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            address = form.cleaned_data['delivery_address']
            phone = form.cleaned_data['phone']

            if qty > product.stock:
                form.add_error('quantity', 'Not enough stock available.')
            else:
                # Create Order
                order = Order.objects.create(
                    customer=request.user,
                    total=product.price * qty,
                    status='pending',
                    delivery_address=address,
                    phone=phone
                )

                # Create OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )

                # Decrement stock and save
                product.stock = product.stock - qty
                product.save()

                messages.success(request, "Order placed successfully.")
                return redirect('orders:confirmation', order_id=order.id)
    else:
        # Prefill form with user info if available
        initial = {
            'quantity': 1,
            'delivery_address': getattr(request.user, 'location', ''),
            'phone': getattr(request.user, 'phone', ''),
        }
        form = CheckoutForm(initial=initial)

    # Safely determine quantity for preview (ensure it's an int)
    if form.is_bound:
        if form.is_valid():
            preview_qty = form.cleaned_data.get('quantity', 1)
        else:
            # form.data values come from POST and are strings; coerce to int safely
            try:
                preview_qty = int(form.data.get('quantity', 1))
            except (TypeError, ValueError):
                preview_qty = int(form.initial.get('quantity', 1))
    else:
        preview_qty = int(form.initial.get('quantity', 1))

    total_preview = product.price * preview_qty
    # Render template
    return render(request, 'checkout.html', {
        'product': product,
        'form': form,
        'total_preview': total_preview,
    })


@login_required
def confirmation(request, order_id):
    # Show order details after placing order
    # Allow the customer who placed the order to view it.
    # Also allow vendors to view the confirmation if the order contains items
    # that belong to them, and allow staff/superuser to view any order.
    order = Order.objects.filter(id=order_id).first()
    if not order:
        messages.error(request, "Order not found.")
        return redirect('products:product_list')

    user_is_customer = (order.customer == request.user)
    user_is_staff = getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False)
    user_is_vendor = getattr(request.user, 'user_type', None) == 'vendor'

    vendor_has_item = False
    if user_is_vendor:
        vendor_has_item = OrderItem.objects.filter(order=order, product__vendor=request.user).exists()

    if not (user_is_customer or user_is_staff or vendor_has_item):
        messages.error(request, "Order not found or you don't have permission to view it.")
        # redirect vendors to their orders list, customers to their orders
        if user_is_vendor:
            return redirect('orders:vendor_orders')
        return redirect('orders:my_orders')

    items = OrderItem.objects.filter(order=order)
    return render(request, 'confirmation.html', {'order': order, 'items': items})

@login_required
def my_orders(request):
    if request.user.user_type != "customer":
        messages.error(request, "Only customers can view this page.")
        return redirect('products:product_list')

    orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {"orders": orders})

#TASK 5.3
@login_required
def vendor_orders(request):
    if request.user.user_type != "vendor":
        messages.error(request, "Only vendors can view this page.")
        return redirect('products:product_list')

    # Get all order items where the product belongs to the logged-in vendor
    vendor_items = OrderItem.objects.filter(product__vendor=request.user)

    # Extract the orders
    orders = {item.order for item in vendor_items}

    return render(request, 'vendor_orders.html', {"orders": orders})

# TASK 5.4
@login_required
def vendor_order_details(request, order_id):
    if request.user.user_type != "vendor":
        messages.error(request, "Only vendors can view this page.")
        return redirect('products:product_list')

    order = get_object_or_404(Order, id=order_id)

    # Filter only the items that belong to this vendor
    items = OrderItem.objects.filter(order=order, product__vendor=request.user)

    return render(request, 'vendor_order_details.html', {
        "order": order,
        "items": items
    })
    



