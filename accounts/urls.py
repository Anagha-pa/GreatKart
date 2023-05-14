from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
    path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('edit_profile/', views.edit_profile,name='edit_profile'),
    path('change_password/', views.change_password,name='change_password'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('myAddress/', views.myAddress, name='myAddress'),
    path('addAddress/', views.addAddress, name='addAddress'),
    path('deleteAddress/<int:id>/', views.deleteAddress, name='deleteAddress'),
    path('editAddress/<int:id>/', views.editAddress, name='editAddress'),
    path('deleteCheckoutAddress/<int:id>/', views.deleteCheckoutAddress, name='deleteCheckoutAddress'),
    path('AddCheckoutAddress/', views.AddCheckoutAddress, name='AddCheckoutAddress'),
   

]

