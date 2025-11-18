from django.db import models
from accounts.models import CustomUser
from products.models import Product

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
    delivery_address = models.TextField()
    phone = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
