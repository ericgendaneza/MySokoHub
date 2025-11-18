# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CheckoutForm
from .models import Order, OrderItem
from products.models import Product

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
        return redirect('products:product_detail', product_id=product.id)  # adjust as needed

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

    total_preview = product.price * (form.initial.get('quantity', 1) if not form.is_bound else form.cleaned_data.get('quantity', 1) if form.is_valid() else form.data.get('quantity', 1))
    # Render template
    return render(request, 'checkout.html', {
        'product': product,
        'form': form,
        'total_preview': total_preview,
    })


@login_required
def confirmation(request, order_id):
    # Show order details after placing order
    order = get_object_or_404(Order, id=order_id, customer=request.user)
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



