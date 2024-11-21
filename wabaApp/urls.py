from django.contrib import admin
from django.urls import path
from wabaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blank-page/', views.blank_page),
    path('index', views.index, name='index'),
]
