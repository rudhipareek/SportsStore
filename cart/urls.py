from django.urls import path
from cart import views
from .views import order_confirmation


app_name = 'cart'
urlpatterns = [
    path('view/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
]
