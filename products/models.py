from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Product(models.Model):
    AVAILABLE = 'available'
    OUT_OF_STOCK = 'out_of_stock'
    DISCONTINUED = 'discontinued'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (OUT_OF_STOCK, 'Out of Stock'),
        (DISCONTINUED, 'Discontinued'),
    ]

    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True, max_length=255)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor} - {self.get_status_display()} - {self.price}"