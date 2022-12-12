from django.urls import  path
from store import views


urlpatterns = [
    path('', views.store, name='store'),
    path('cartegory/<slug:product_slug>/', views.store, name='product_by_cartegory'),
    path('cartegory/<slug:cartegory_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
    path('serach/', views.search, name='search'),
]