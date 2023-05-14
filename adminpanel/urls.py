from django.urls import path
from .import views 


urlpatterns = [
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admin_dashboard/', views.dashbord, name='admin_dashboard'),
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),

]