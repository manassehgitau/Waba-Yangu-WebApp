from django.contrib import admin
from wabaApp.models import ContactMessage, Customer, Admin, Employee

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Employee)

