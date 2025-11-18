from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
class CustomUser(AbstractUser):
    user_type = models.TextField(choices=[('vendor', 'Vendor'), ('customer','Customer')])
    email = models.EmailField()
    phone = models.TextField()
    location = models.TextField()
    def __str__(self):
        return(f"user_typ:{self.user_type}\nemail:{self.email}\nphone:{self.phone}\nlocation:{self.location}")


