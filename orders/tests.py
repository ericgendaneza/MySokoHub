from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import Product
from .models import Order, OrderItem


class CartAndCheckoutTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(username='cust', password='pass', user_type='customer')
		# create a vendor to satisfy product FK
		self.vendor = User.objects.create_user(username='vend', password='pass', user_type='vendor')
		self.product = Product.objects.create(name='Widget', price=Decimal('100.00'), stock=5, status='active', vendor=self.vendor)

	def test_add_to_cart_and_view(self):
		self.client.login(username='cust', password='pass')
		url = reverse('orders:add_to_cart', args=[self.product.id])
		resp = self.client.post(url, {'quantity': 2}, follow=True)
		self.assertEqual(resp.status_code, 200)
		session = self.client.session
		self.assertIn(str(self.product.id), session.get('cart', {}))
		self.assertEqual(session['cart'][str(self.product.id)], 2)

	def test_product_list_shows_unit_and_add_from_list(self):
		# product list shows unit
		resp = self.client.get(reverse('products:product_list'))
		self.assertContains(resp, f'/ {self.product.unit}')

		# adding from product list works (default qty 1)
		self.client.login(username='cust', password='pass')
		resp = self.client.post(reverse('orders:add_to_cart', args=[self.product.id]), follow=True)
		self.assertEqual(resp.status_code, 200)
		session = self.client.session
		self.assertEqual(session['cart'][str(self.product.id)], 1)

	def test_anonymous_add_to_cart_and_view(self):
		# No login, add product
		resp = self.client.post(reverse('orders:add_to_cart', args=[self.product.id]), {'quantity': 2}, follow=True)
		self.assertEqual(resp.status_code, 200)
		session = self.client.session
		self.assertIn(str(self.product.id), session.get('cart', {}))
		self.assertEqual(session['cart'][str(self.product.id)], 2)

		# Anonymous can view cart page
		resp = self.client.get(reverse('orders:cart_view'))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, self.product.name)

	def test_checkout_cart_creates_order(self):
		self.client.login(username='cust', password='pass')
		# put item in session
		session = self.client.session
		session['cart'] = {str(self.product.id): 3}
		session.save()

		url = reverse('orders:checkout_cart')
		resp = self.client.get(url, follow=True)
		self.assertEqual(resp.status_code, 200)

		orders = Order.objects.filter(customer=self.user)
		self.assertEqual(orders.count(), 1)
		order = orders.first()
		items = OrderItem.objects.filter(order=order)
		self.assertEqual(items.count(), 1)
		item = items.first()
		self.assertEqual(item.quantity, 3)

		# product stock decremented
		self.product.refresh_from_db()
		self.assertEqual(self.product.stock, 2)
