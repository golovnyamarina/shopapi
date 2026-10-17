from django.contrib import admin
from django.urls import path
from store import views
urlpatterns = [
    path('products/', views.products_list, name='products_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/price/', views.product_update_price, name='product_update_price'),
    path('orders/create/',views.order_create, name='order_create'),
    path('customers/<int:pk>/orders/', views.customer_orders, name='customer_orders'),
    path('stats/categories/', views.category_stats, name='category_stats'),
    path('discount/', views.discount_view, name='discount'),
]