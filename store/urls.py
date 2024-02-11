from django.urls import path
from . import views
from .views import SalesList

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sales/', SalesList.as_view(), name='sales'),
    path('place_order/', views.place_order, name='place_order'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_customers/', views.view_customers, name='view_customers'),
    path('view_products/', views.view_products, name='view_products'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('receipt/<int:pk>/', views.receipt, name='receipt'),
]