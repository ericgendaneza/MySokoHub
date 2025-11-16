from django.urls import path
from .views import *
#from django.contrib.auth import authenticate, login, logout

urlpatterns = [
    path('accounts/login/', login,name='login'),
    path('', welcome,name='welcome'),
    path('acounts/logout/', logout,name='logout'),
    path('register/', register_view, name='register'),

    

]