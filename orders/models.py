from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Orders(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.IntegerField()
    status = models.TextField()
    delivery_adress = models.TextField()
    phone = models.TextField(max_length=14, min=10)
    created_at = models.DateTimeField(auto_now=True)
    
    



