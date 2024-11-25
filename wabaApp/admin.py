from django.contrib import admin
from wabaApp.models import ContactMessage, Customer, Admin, Employee, WaterUsage, PrepaidBalance, LeakDetection, Payment, Notification

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
