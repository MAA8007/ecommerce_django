from django.urls import path
from . import views
from .views import Register

urlpatterns = [
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('update_cart_item/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('payment_result/', views.payment, name='payment_result'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('register/', Register.as_view(), name='register'),
    path('products/', views.product_list, name='product_list'),
    path('', views.home, name='home'),
    path('products/<int:category_id>/', views.product_list, name='product_list_by_category'),
   


]
