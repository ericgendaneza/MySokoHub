import os
import django
import sys

# Ensure project root is on sys.path so the `SokoHub` package can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SokoHub.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

# Create a test customer if not exists
username = 'test_customer'
password = 'testpass123'
user, created = User.objects.get_or_create(username=username, defaults={'user_type': 'customer', 'email': 'test@example.com'})
if created:
    user.set_password(password)
    user.save()
    print('Created test customer')
else:
    # Ensure password matches for login attempt
    user.set_password(password)
    user.save()

# Ensure a product with id=1 exists
product, pcreated = Product.objects.get_or_create(id=1, defaults={'name': 'Test Product', 'description': 'Auto-created product', 'price': 1000.00, 'stock': 10, 'vendor': user})
if pcreated:
    print('Created test product with id=1')

client = Client()
logged_in = client.login(username=username, password=password)
print('Logged in:', logged_in)

# Attempt checkout POST
url = '/orders/checkout/1/'
resp = client.post(url, {'quantity': '2', 'delivery_address': '123 Main', 'phone': '0788123456'}, follow=True, HTTP_HOST='127.0.0.1')
print('POST', url, '=> status', resp.status_code)
if resp.redirect_chain:
    print('Redirect:', resp.redirect_chain)

# Print a short excerpt of the response content
content = resp.content.decode('utf-8', errors='replace')
print('Response excerpt:')
print(content[:1500])

# Show created orders for the user
from orders.models import Order, OrderItem
orders = Order.objects.filter(customer=user)
print('Orders for user:', orders.count())
for o in orders:
    print('Order', o.id, 'total', o.total, 'status', o.status)
    for it in OrderItem.objects.filter(order=o):
        print(' -', it.product.name, 'qty', it.quantity, 'price', it.price)
