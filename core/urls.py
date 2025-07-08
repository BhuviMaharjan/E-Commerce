from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/approve/<int:user_id>/', views.approve_seller, name='approve_seller'),
    path('admin-dashboard/block/<int:user_id>/', views.block_user, name='block_user'),
    path('admin-dashboard/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('admin-dashboard/role/<int:user_id>/', views.change_user_role, name='change_user_role'),
    path('admin-dashboard/add/', views.add_user, name='add_user'),
    path('admin-dashboard/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin-dashboard/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-dashboard/profile/', views.admin_profile_dashboard, name='admin_profile_dashboard'),
] 