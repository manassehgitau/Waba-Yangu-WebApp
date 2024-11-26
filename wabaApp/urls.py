from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from wabaApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blankpage/', views.blank_page, name='blankpage'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('404/', views.page_not_found, name='404'),
    path('loginadmin/', views.login_admin, name='loginadmin'),
    path('loginemployee/', views.login_employee, name='loginemployee'),
    path('register/', views.register, name='register'),
    path('customerdashboard/<int:customer_id>/', views.customerdashboard, name='customerdashboard'),
    path('productslist/<int:customer_id>/', views.productslist, name='productslist'),
    path('cart/<int:customer_id>/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/<int:customer_id>', views.add_to_cart, name='add_to_cart'),
    path('employeedashboard/', views.employeedashboard, name='employeedashboard'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('productscheckout/', views.productscheckout, name='productscheckout'),
    path('productsinglelist/', views.productsinglelist, name='productsinglelist'),
    path('customerinvoice/', views.customerinvoice, name='customerinvoice'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
]

