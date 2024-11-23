from django.shortcuts import render, redirect
from wabaApp.models import ContactMessage, Customer
from django.contrib import messages
from wabaApp.forms import ContactForm

# Create your views here.
def blank_page(request):
    return render(request, 'blank-page.html')

def index(request):
    if request.method == 'POST':
        contacts_acquired = ContactMessage(
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['message'],
        )
        contacts_acquired.save()
        messages.success(request, 'Your message has been sent successfully.')
        return redirect('index')
    else:
        return render(request, 'index.html',  {'messages': messages.get_messages(request)})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(username=username)
            if customer.password == password:
                # Successfully logged in
                messages.success(request, 'You are logged in successfully.')
                return redirect('home')  # Replace 'home' with your desired page
            else:
                messages.error(request, 'Incorrect password.')
        except Customer.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'login.html')

def login_admin(request):
    return render(request, 'loginadmin.html')

def login_employee(request):
    return render(request, 'loginemployee.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        # Check if the user already exists
        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        # Create a new customer
        new_customer = Customer(username=username, email=email, phone=phone, password=password)
        new_customer.save()
        messages.success(request, 'You have been registered successfully.')
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'register.html')

def forgotpassword(request):
    return render(request, 'customer-forgot-password.html')

def employeedashboard(request):
    return render(request, 'employee-dashboard.html')

def customerdashboard(request):
    return render(request, 'admin-dashboard.html')

def admindashboard(request):
    return render(request, 'customer-dashboard.html')

def productscheckout(request):
    return render(request, 'customer-product-checkout.html')

def productslist(request):
    return render(request, 'customer-product-list.html')

def productsinglelist(request):
    return render(request, 'customer-product-single-list.html')

def customerinvoice(request):
    return render(request, 'invoice.html')

