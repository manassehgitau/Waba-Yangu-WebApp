from django.contrib import admin
from django.urls import path
from wabaApp import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('employeedashboard/', views.employeedashboard, name='employeedashboard'),
    path('admindashboard/<int:admin_id>/', views.admindashboard, name='admindashboard'),
    path('adminproducts/<int:admin_id>/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('productscheckout/', views.productscheckout, name='productscheckout'),
    path('productsinglelist/', views.productsinglelist, name='productsinglelist'),
    path('productslist/<int:customer_id>/', views.productslist, name='productslist'),
    path('invoice/<int:sale_id>/', views.generate_invoice, name='generate_invoice'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

