from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name='store'),
    path('Category/<slug:category_slug>/',views.store, name='products_by_category'),
    path('Category/<int:id>/product_detail',views.product_detail, name='product_detail'),
    path('search/', views.search, name='search' ),
    path('price_sort',views.price_sort,name='price_sort'),
    path('filter_price/',views.filter_price,name='filter_price'),
    path('product_review/<int:id>/',views.product_review,name='product_review'),


]