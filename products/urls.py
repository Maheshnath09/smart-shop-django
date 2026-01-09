from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),  # Must be before category slug
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]