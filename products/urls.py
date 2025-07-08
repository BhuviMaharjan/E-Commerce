from django.urls import path
from . import views
from .views import add_category, add_tag

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('my/', views.manage_products, name='manage_products'),
    path('add-category/', add_category, name='add_category'),
    path('add-tag/', add_tag, name='add_tag'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('manage-tags/', views.manage_tags, name='manage_tags'),
    path('edit-tag/<int:pk>/', views.edit_tag, name='edit_tag'),
    path('delete-tag/<int:pk>/', views.delete_tag, name='delete_tag'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('orders/', views.seller_orders, name='seller_orders'),
    path('orders/mark-delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),
] 