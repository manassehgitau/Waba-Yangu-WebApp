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
    path('product/<int:product_id>/<int:customer_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/<int:customer_id>/', views.add_to_cart, name='add_to_cart'),
    path('employeedashboard/', views.employeedashboard, name='employeedashboard'),
    path('admindashboard/<int:admin_id>/', views.admindashboard, name='admindashboard'),
    path('adminproducts/<int:admin_id>/', views.admin_product_list, name='admin_product_list'),
    path('edit/<int:product_id>/<int:admin_id>/', views.edit_product, name='edit_product'),
    path('productscheckout/', views.productscheckout, name='productscheckout'),
    path('productsinglelist/', views.productsinglelist, name='productsinglelist'),
    path('productslist/<int:customer_id>/', views.productslist, name='productslist'),
    path('invoice/<int:customer_id>/', views.generate_invoice, name='generate_invoice'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('report/<int:customer_id>/', views.customer_report, name='customer_report'),
    path('payments/<int:customer_id>/', views.customer_payments, name='customer_payments'),

    path('pay/<int:customer_id>/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

    path('accountmanagement/<int:customer_id>/', views.account_management, name='account_management'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


