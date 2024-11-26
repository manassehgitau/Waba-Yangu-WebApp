from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from wabaApp.models import ContactMessage, Customer, Admin, Employee, WaterUsage, PrepaidBalance, LeakDetection, Payment, Notification, Product, CartItem, Sale
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
import math
from wabaApp.forms import ContactForm

# Create your views here.
def page_not_found(request):
    return render(request, '404.html')

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
                return HttpResponseRedirect(f'/customerdashboard/{customer.id}/')
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


'''
    This is for testing purposes only (it does not go to a database)
'''
# @login_required(login_url='login')
# def customerdashboard(request, customer_id):
#     try:
#         # Get customer and data from the database
#         customer = Customer.objects.get(id=customer_id)
#
#         # Simulate data or query real data
#         data = {
#             'water_usage_today': 120,  # Today's usage (replace with actual query)
#             'prepaid_balance': 450,  # Current balance (replace with actual query)
#             'leak_detection': 'No Leaks',  # Latest leak status (replace with actual query)
#             'meter_status': 'Operational',  # Meter status (replace with actual query)
#             'payment_history': [
#                 {'amount': 500, 'date': '2024-11-21'},
#                 {'amount': 300, 'date': '2024-11-13'}
#             ],
#             'water_usage_week': [100, 150, 120, 200, 170, 220, 180],  # Water usage for the last 7 days
#             'balance_trend_week': [450, 420, 430, 410, 400, 380, 450],  # Balance for the last 7 days
#             'notifications': [
#                 'Low balance! Please top up.',
#                 'You have reached 80% of your monthly water usage goal.'
#             ],
#             'water_savings': 10,  # Example water savings in percentage
#             'support_contact': 'support@example.com'  # Support contact info
#         }
#
#         # Pass the data to the template
#         return render(request, 'customer-dashboard.html', {'customer': customer, 'dashboard_data': data})
#
#     except Customer.DoesNotExist:
#         return render(request, '404.html')  # Handle customer not found

'''
    This is for Product purposes (it must have a database)
'''

@login_required(login_url='login')
def customerdashboard(request, customer_id):
    try:
        customer = get_object_or_404(Customer, id=customer_id)
        # Get the customer object
        customer = Customer.objects.get(id=customer_id)

        # Fetch today's water usage (latest entry)
        water_usage_today = WaterUsage.objects.filter(customer=customer, date=timezone.now().date()).first()
        water_usage_today_value = water_usage_today.usage if water_usage_today else 0

        # Fetch the prepaid balance
        prepaid_balance = PrepaidBalance.objects.filter(customer=customer).first()
        balance = prepaid_balance.balance if prepaid_balance else 0

        # Define cost per liter of water (for calculation)
        cost_per_liter = 5  # Assume 1 liter of water costs 5 KSh

        # Calculate expected water usage (based on prepaid balance)
        expected_usage = balance / cost_per_liter  # Calculate how many liters the customer should be able to use based on balance

        # Calculate actual usage for today
        actual_usage = water_usage_today_value

        # Calculate water savings (as a percentage)
        if expected_usage > 0:
            water_savings = ((expected_usage - actual_usage) / expected_usage) * 100
        else:
            water_savings = 0  # In case no data is available or the expected usage is zero

        # Fetch recent payment history (last 2 payments)
        recent_payments = Payment.objects.filter(customer=customer).order_by('-date')[:2]
        payment_history = [{'amount': payment.amount, 'date': payment.date.strftime('%Y-%m-%d')} for payment in recent_payments]

        # Fetch water usage for the last 7 days (for the graph)
        water_usage_week = WaterUsage.objects.filter(customer=customer, date__gte=timezone.now() - timedelta(days=0)).values_list('usage', flat=True)
        water_usage_week = list(water_usage_week)

        # Fetch balance trend for the last 7 days
        balance_trend_week = PrepaidBalance.objects.filter(customer=customer, date__gte=timezone.now() - timedelta(days=0)).values_list('balance', flat=True)
        balance_trend_week = list(balance_trend_week)

        # Fetch notifications for the customer (dynamic data)
        notifications = Notification.objects.filter(customer=customer, read=False).order_by('-created_at')

        # Support contact info (this could be dynamic based on customer data or fixed)
        support_contact = 'support@example.com'

        # Pass the data to the template
        data = {
            'water_usage_today': water_usage_today_value,
            'prepaid_balance': balance,
            'leak_detection': 'No Leaks',  # Replace with dynamic data if available
            'meter_status': "Operational",  # Static for now
            'payment_history': payment_history,
            # testing
            'water_usage_week': [100, 150, 120, 200, 170, 220, 180],  # Water usage for the last 7 days
            'balance_trend_week': [450, 420, 430, 410, 400, 380, 450],  # Balance for the last 7 days
            # with database
            # 'water_usage_week': water_usage_week,
            # 'balance_trend_week': balance_trend_week,
            'notifications': notifications,
            'water_savings': round(water_savings),
            'support_contact': support_contact
        }

        return render(request, 'customer-dashboard.html', {'customer': customer, 'dashboard_data': data, 'customer_id': customer.id})

    except Customer.DoesNotExist:
        return render(request, '404.html')  # Handle customer not found

# Cart View
@login_required
def cart_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = CartItem.objects.filter(customer=customer)  # Assuming user refers to Customer
    total_price = sum([item.get_total_price() for item in cart_items])  # Fixed typo
    return render(request, 'add_to_cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Product List View
def productslist(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    products = Product.objects.all()  # Correct filter method
    return render(request, 'customer-product-list.html', {'products': products, 'customer': customer})

@login_required
# Add to Cart View
def add_to_cart(request, product_id, customer_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, id=customer_id)
    cart_item, created = CartItem.objects.get_or_create(customer=customer, product=product)  # Assuming user is linked to Customer
    cart_item.quantity += 1
    cart_item.save()
    return redirect('productslist', customer_id=customer_id)  # Redirect back to the product list with the customer's ID

@login_required
def process_sale(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = CartItem.objects.filter(customer=customer)
    if cart_items:
        total_price = sum([item.get_total_price() for item in cart_items])
        sale = Sale.objects.create(customer=customer, total_price=total_price)
        cart_items.delete()  # Clear cart after sale
    return redirect('admindashboard', customer_id=customer_id)

@login_required(login_url='loginadmin')
def admindashboard(request):

@login_required(login_url='loginemployee')
def employeedashboard(request):
    return render(request, 'employee-dashboard.html')



def productscheckout(request):
    return render(request, 'customer-product-checkout.html')

def productsinglelist(request):
    return render(request, 'customer-product-single-list.html')

def customerinvoice(request):
    return render(request, 'invoice.html')
