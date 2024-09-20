from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.user_signup, name='register')
]