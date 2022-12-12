from django.urls import path
from cart import views 

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('minusCart/<int:product_id>/<int:cart_item_id>/', views.minusCart, name='minusCart'),
    path('removeCart/<int:product_id>/<int:cart_item_id>/', views.removeCart, name='removeCart'),
    path('checkout/', views.checkout, name='checkout'),
]