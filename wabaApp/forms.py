from django import forms
from wabaApp.models import Product, CustomerReport, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']

class CustomerReportForm(forms.ModelForm):
    class Meta:
        model = CustomerReport
        fields = ['issue_type', 'issue_description', 'file_attachment', 'email']  # Define the fields to include in the form
        widgets = {
            'issue_description': forms.Textarea(attrs={'rows': 5}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }