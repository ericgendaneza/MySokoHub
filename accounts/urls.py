from django.urls import path
from .views import welcome, login

urlpatterns = [
    path('welcome/', welcome),
    path('login/', login)
]