from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Products(models.Model):
    vendor = models.ForeignKey(CustomUser, on_delete=models.RESTRICT) #you will have to change it to CASCADE for testing purposes
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField()
    status = models.TextField()
    created_at = models.DateTimeField(auto_now=True)