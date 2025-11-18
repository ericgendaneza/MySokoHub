from django.db import models
from accounts.models import CustomUser
from products.models import Product

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.IntegerField()
    status = models.TextField()
    delivery_address = models.TextField()
    phone = models.TextField(max_length=14)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return (f"Customer: {self.customer}\ntotal:{self.total}\nstatus:{self.status}\ndelivery_adress:{self.delivery_adress}\nphone:{self.phone}\ncreated_at:{self.created_at}")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
