from django.urls import path
from .views import welcome, login

urlpatterns = [
    path('login/', login),
    path('welcome/', welcome)
]