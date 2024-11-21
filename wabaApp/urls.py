from django.contrib import admin
from django.urls import path
from wabaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blank-page/', views.blank_page),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('loginadmin/', views.login_admin, name='loginadmin'),
    path('register/', views.register, name='register'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),
]
