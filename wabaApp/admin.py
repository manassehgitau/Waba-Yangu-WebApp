from django.contrib import admin
from wabaApp.models import ContactMessage, Customer, Admin, Employee, WaterUsage, PrepaidBalance, LeakDetection, Payment, Notification, Sale, Product, Refund, CartItem, Invoice

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(Admin)
admin.site.register(Employee)
admin.site.register(WaterUsage)
admin.site.register(PrepaidBalance)
admin.site.register(LeakDetection)
admin.site.register(Payment)
admin.site.register(Notification)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone')  # Columns to display in the admin list view
    search_fields = ('username', 'email')  # Allow searching by username and email
    filter_horizontal = ('products',)  # Display the products many-to-many relation in a horizontal widget

# Register Customer model with the customized CustomerAdmin
admin.site.register(Customer, CustomerAdmin)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'sale_date', 'total_price')
    list_filter = ('sale_date', 'product')
    search_fields = ('customer__username', 'product__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')  # Fields to display in the admin list view
    search_fields = ('name',)  # Allow searching by product name
    list_filter = ('price',)  # Filter products by price
    ordering = ('-price',)  # Order products by price in descending order
    fields = ('name', 'price', 'description', 'image')  # Fields for adding or editing products in the form

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('sale', 'refund_amount', 'status', 'refund_date')
    list_filter = ('status',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'get_total_price')  # Display cart item details
    list_filter = ('customer', 'product')  # Filters for customer and product
    search_fields = ('customer__username', 'product__name')  # Allow search by customer or product name

# Register the Invoice model
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sale', 'issue_date', 'total_amount')  # Show columns in the list view
    list_filter = ('issue_date', 'customer')  # Filter options
    # search_fields = ('customer__username', 'sale__id')  # Searchable