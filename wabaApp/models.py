from django.contrib.auth.hashers import make_password
from django.db import models
from datetime import timedelta

# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

class WaterUsage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    usage = models.DecimalField(max_digits=10, decimal_places=2)  # Water usage in liters

    def __str__(self):
        return f"Water Usage for {self.customer} on {self.date}"

class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)  # Track if the user has read the notification
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the time when the notification was created

    def __str__(self):
        return self.message


class PrepaidBalance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Prepaid balance in KSh
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prepaid balance for {self.customer} on {self.date}"


class LeakDetection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # True for leak detected, False for no leak
    detection_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leak Detection for {self.customer} on {self.detection_date}"


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount in KSh
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.customer} on {self.date}"

class Product(models.Model):
    product_name =  models.CharField(max_length=200)
    description = models.TextField()
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name

class CartItem(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.product.product_name}'

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    items=models.ManyToManyField(CartItem)
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order{self.id} - {self.customer.username}"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.product.product_name} by {self.customer.username}"

class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    admin_id = models.CharField(max_length=50)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.username