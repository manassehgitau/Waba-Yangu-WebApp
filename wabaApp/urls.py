from django.contrib import admin
from django.urls import path
from wabaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blankpage/', views.blank_page, name='blankpage'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('loginadmin/', views.login_admin, name='loginadmin'),
    path('loginemployee/', views.login_employee, name='loginemployee'),
    path('register/', views.register, name='register'),
    path('employeedashboard/', views.employeedashboard, name='employeedashboard'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('productscheckout/', views.productscheckout, name='productscheckout'),
    path('productslist/', views.productslist, name='productslist'),
    path('productsinglelist/', views.productsinglelist, name='productsinglelist'),
    path('customerinvoice/', views.customerinvoice, name='customerinvoice'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
]
