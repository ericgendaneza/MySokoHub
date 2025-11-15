from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    user_type = models.TextField(choices=[('vendor', 'Vendor'), ('customer','Customer')])
    email = models.EmailField()
    phone = models.TextField()
    location = models.TextField()


