from django.contrib import admin
from wabaApp.models import ContactMessage, Customer, Admin

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(Customer)
admin.site.register(Admin)
