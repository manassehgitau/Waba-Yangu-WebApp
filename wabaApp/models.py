from django.db import models

# Create your models here.
class Employee(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    admin_id = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name