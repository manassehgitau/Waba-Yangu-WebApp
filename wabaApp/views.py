from django.shortcuts import render, redirect
from wabaApp.models import ContactMessage, Customer, Admin, Employee
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
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

            if check_password(password, customer.password):
                # Successfully logged in
                messages.success(request, 'You are logged in successfully.')
                return redirect('customerdashboard')
            else:
                messages.error(request, 'Incorrect password.')
        except Customer.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

            # Check if the user already exists
        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        # Hash the password before saving it to the database
        hashed_password = make_password(password)

        # Create a new customer
        new_customer = Customer(username=username, email=email, phone=phone, password=hashed_password)
        new_customer.save()
        messages.success(request, 'You have been registered successfully.')
        return redirect('login')

    return render(request, 'register.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin_id = request.POST['admin_id']

        try:
            admin = Admin.objects.get(username=username)

            if password == admin.password:
                # Successfully logged in
                if  admin_id == admin.admin_id:
                    messages.success(request, 'You are logged in successfully.')
                    return redirect('admindashboard')
                else:
                    messages.error(request, 'Incorrect admin ID.')
            else:
                messages.error(request, 'Incorrect password.')
        except Admin.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'loginadmin.html')


def login_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        employee_id = request.POST['employee_id']
        try:
            employee = Employee.objects.get(username=username)

            if password == employee.password:
                # Successfully logged in
                if employee_id == employee.employee_id:
                    messages.success(request, 'You are logged in successfully.')
                    return redirect('employeedashboard')
                else:
                    messages.error(request, 'Incorrect employee ID.')
            else:
                messages.error(request, 'Incorrect password.')
        except Employee.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'loginemployee.html')

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

