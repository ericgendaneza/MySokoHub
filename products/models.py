from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Product(models.Model):
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #you will have to change it to CASCADE for testing purposes
    name= models.CharField(max_length=225, default='User')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return(f"vendor:{self.vendor}\ndescription:{self.description}\nprice:{self.price}\nstock:{self.stock}\nimage:{self.image}\nstatus:{self.status}\ncreated_at:{self.created_at}")