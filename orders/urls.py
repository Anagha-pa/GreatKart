from django.urls import path
from orders import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('payments/', views.payments, name='payments'),
    path("coupons/",views.coupons,name='coupons'),
    path("cash_on_delivery/<int:id>/",views.cash_on_delivery,name='cash_on_delivery'),
    
    path("cancel_order/<int:id>/",views.cancel_order,name='cancel_order'),   
    path("return_order/<int:id>/",views.return_order,name='return_order'), 

]