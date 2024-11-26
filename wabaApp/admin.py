from django.contrib import admin
from wabaApp.models import ContactMessage, Customer, Admin, Employee, WaterUsage, PrepaidBalance, LeakDetection, Payment, Notification, Product, CartItem, Order, Sale

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Employee)
admin.site.register(WaterUsage)
admin.site.register(PrepaidBalance)
admin.site.register(LeakDetection)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Sale)
