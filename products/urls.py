from django.urls import path

from products import views



urlpatterns=[
    path('search/', views.search_products, name='search_products'),
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('', views.show_products, name='show_products'),
]