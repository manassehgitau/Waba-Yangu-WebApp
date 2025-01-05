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
    path('employees/', views.employee_list, name='employee_list'),

    path('register/', views.register, name='register'),
    path('customerdashboard/<int:customer_id>/', views.customerdashboard, name='customerdashboard'),
    path('product/<int:product_id>/<int:customer_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('employeedashboard/', views.employeedashboard, name='employeedashboard'),
    path('admindashboard/<int:admin_id>/', views.admindashboard, name='admindashboard'),
    path('adminproducts/', views.admin_product_list, name='admin_product_list'),
    path('productscheckout/', views.productscheckout, name='productscheckout'),
    path('productsinglelist/', views.productsinglelist, name='productsinglelist'),
    path('productslist/<int:customer_id>/', views.productslist, name='productslist'),
    path('invoice/<int:customer_id>/', views.generate_invoice, name='generate_invoice'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('report/<int:customer_id>/', views.customer_report, name='customer_report'),
    path('payments/<int:customer_id>/', views.customer_payments, name='customer_payments'),

    path('pay', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

    path('accountmanagement/<int:customer_id>/', views.account_management, name='account_management'),
    path('editadminproducts/<int:product_id>/', views.edit_product),  # Edit product URL
    path('deleteadminproducts/<int:product_id>/', views.delete_product),  # Edit product URL

    path('admincustomers/<int:admin_id>/', views.admin_customer_list, name='admin_customer_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


