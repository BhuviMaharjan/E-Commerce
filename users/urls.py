from django.urls import path
from . import views
from .views import edit_profile

urlpatterns = [
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('edit_profile/', edit_profile, name='edit_profile'),
] 