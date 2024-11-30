import requests
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import json

from django.shortcuts import render, redirect, get_object_or_404
from wabaApp.models import ContactMessage, Customer, Admin, Employee, WaterUsage, PrepaidBalance, LeakDetection, Payment, Notification, Sale, Refund, Product, CartItem, Invoice
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from wabaApp.forms import ProductForm, CustomerReportForm, CustomerForm
from django.db import models
from wabaApp.credentials import LipanaMpesaPpassword, MpesaAccessToken

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
                    return HttpResponseRedirect(f'/admindashboard/{admin.id}/')
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

def admindashboard(request, admin_id):
    try:
        admin = get_object_or_404(Customer, id=admin_id)
        # Get the customer object
        admin = Customer.objects.get(id=admin_id)

        sales = Sale.objects.all()
        refunds = Refund.objects.all()  # Get all refunds

        total_customers = Customer.objects.count()
        total_revenue = sum(sale.total_price for sale in sales)
        total_refund_amount = sum(refund.refund_amount for refund in refunds)  # Total refund amount
        total_refunds = refunds.count()
        recent_sales = Sale.objects.filter(sale_date__gte=timezone.now() - timedelta(days=7)).order_by('-sale_date')[:10]  # Last 10 recent sales

        # # Get customer growth over the last 7 days (daily new customers count)
        # customer_growth = []
        # for i in range(7):
        #     date = timezone.now() - timedelta(days=i)
        #     count = Customer.objects.filter(date_joined__date=date.date()).count()  # Filter by the date joined
        #     customer_growth.append({'date': date.strftime('%Y-%m-%d'), 'count': count})
        #
        # # Calculate water savings over the last 7 days
        # water_savings_data = []
        # baseline_usage = 100  # Set a fixed baseline, e.g., 100 liters per day. Adjust according to your logic.
        #
        # for i in range(7):
        #     date = timezone.now() - timedelta(days=i)
        #     # Get the total water usage for each day
        #     water_usage = WaterUsage.objects.filter(date=date.date()).aggregate(total_usage=Sum('usage'))[
        #                       'total_usage'] or 0
        #     # Calculate savings (example: savings = baseline - actual usage)
        #     savings = max(0, baseline_usage - water_usage)
        #     water_savings_data.append({'date': date.strftime('%Y-%m-%d'), 'savings': savings})

        # Dummy customer growth over the last 7 days (assume 10 new customers per day)
        customer_growth = []
        for i in range(7):
            date = timezone.now() - timedelta(days=i)
            count = 10  # Assume 10 new customers per day for testing
            customer_growth.append({'date': date.strftime('%Y-%m-%d'), 'count': count})

        # Dummy water savings data (assume baseline of 100 liters per day and 50 liters used per day)
        water_savings_data = []
        baseline_usage = 100  # baseline usage is 100 liters
        for i in range(7):
            date = timezone.now() - timedelta(days=i)
            water_usage = 50  # Assume 50 liters of water usage per day for testing
            savings = max(0, baseline_usage - water_usage)  # Savings calculation
            water_savings_data.append({'date': date.strftime('%Y-%m-%d'), 'savings': savings})

        data = {
            'total_customers': total_customers,
            'total_revenue': total_revenue,
            'total_refund_amount': total_refund_amount,
            'total_refunds': total_refunds,
            'recent_sales': recent_sales,
            'water_savings_data': water_savings_data,
            'customer_growth_data': customer_growth,

        }

        return render(request, 'admin-dashboard.html', {'admin': admin, 'dashboard_data': data, 'admin_id': admin.id})

    except Admin.DoesNotExist:
        return render(request, '404.html')  # Handle customer not found

def admin_product_list(request, admin_id):
    admin = Customer.objects.get(id=admin_id)  # Fetch the customer (You can use get_object_or_404 too)
    products = Product.objects.all()  # Fetch all products
    return render(request, 'admin-product-management.html', {'products': products, 'admin': admin})

def edit_product(request, product_id, admin_id):
    update_product = Product.objects.get(id=product_id)
    form = ProductForm(request.POST, instance=update_product)
    if form.is_valid():
        form.save()
        return redirect('adminproducts', admin_id)
    else:
        return render(request, 'edit-product.html')

def productslist(request, customer_id):
    customer = Customer.objects.get(id=customer_id)  # Fetch the customer (You can use get_object_or_404 too)
    products = Product.objects.all()  # Fetch all products
    return render(request, 'customer-product-list.html', {'products': products, 'customer': customer})


# View for displaying product details and adding to cart
def product_detail(request, product_id, customer_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, id=customer_id)

    return render(request, 'product-detail.html', {'product': product, 'customer': customer})


# View for adding a product to the cart
def add_to_cart(request, product_id, customer_id):
    product = Product.objects.get(id=product_id)
    customer = get_object_or_404(Customer, id=customer_id)

    # Get or create CartItem for the customer and product
    cart_item, created = CartItem.objects.get_or_create(customer=customer, product=product)

    # If cart item exists, increase the quantity
    cart_item.quantity += 1
    cart_item.save()

    return redirect('product_detail', product_id=product.id, customer_id=customer.id)


def productsinglelist(request):
    return render(request, 'customer-product-single-list.html')


def generate_invoice(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Fetch all invoices for the customer
    invoices = Invoice.objects.filter(customer=customer)

    # You can sum the total amounts, or loop through each sale if needed
    total_amount = sum(invoice.total_amount for invoice in invoices)

    # You might want to loop through each sale for displaying individual sale details in the invoice
    sales = Sale.objects.filter(customer=customer)

    discount_percentage = Decimal('0.2')  # Assuming the discount is 20%
    discounts = []
    for sale in sales:
        discount = sale.total_price * discount_percentage
        discounts.append(discount)

    # Render the invoice page, passing the invoices and sales data
    return render(request, 'invoice.html', {
        'invoices': invoices,
        'customer': customer,
        'sales': sales,
        'discounts': discounts,
        'total_amount': total_amount,
    })

@login_required(login_url='loginemployee')
def employeedashboard(request):
    return render(request, 'employee-dashboard.html')

def productscheckout(request):
    return render(request, 'customer-product-checkout.html')

@login_required
def customer_report(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)  # Assuming User is used for customers

    if request.method == 'POST':
        form = CustomerReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.customer = customer  # Assign the customer
            report.save()
            return redirect('customerdashboard', customer_id=customer.id)  # Redirect after submission
    else:
        form = CustomerReportForm()

    return render(request, 'customer-report.html', {'form': form, 'customer': customer})

def customer_payments(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)  # Get customer by ID
    payments = Payment.objects.filter(customer=customer)  # Get all payments for the customer

    # Calculate the total payments made by the customer
    total_paid = payments.aggregate(models.Sum('amount'))['amount__sum'] or 0

    # Pass the payments and total paid to the template
    return render(request, 'customer_payments.html', {
        'customer': customer,
        'payments': payments,
        'total_paid': total_paid
    })


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'prepaid-mpesa.html', {'customer': customer})

def stk(request):
    if request.method =="POST":
        phone = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        if phone and amount:
            try:
                customer = get_object_or_404(Customer, phone=phone)  # Optionally match customer by phone number

                # Process payment (mock example for success)
                payment = Payment(
                    customer=customer,
                    phone_number=phone,
                    amount=Decimal(amount),
                    payment_method="Lipa na M-Pesa"
                )
                payment.save()

                # Update the customer's prepaid balance by creating a new PrepaidBalance entry
                # If the customer already has a balance record, we fetch the latest one to update
                current_balance = PrepaidBalance.objects.filter(customer=customer).last()

                if current_balance:
                    new_balance = current_balance.balance + Decimal(amount)
                else:
                    new_balance = Decimal(amount)  # If no previous balance, set current balance to the payment amount

                # Create a new PrepaidBalance entry for the customer
                PrepaidBalance.objects.create(
                    customer=customer,
                    balance=new_balance
                )


                messages.success(request, f"Payment of Kshs {amount} was successful!")
                # return redirect('customerdashboard')  # Redirect to a success page or confirmation page
            except Exception as e:
                messages.error(request, f"Payment failed: {str(e)}")
                # return redirect('make_payment')  # Redirect to the payment page again

        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse('/customerdashboard')


def account_management(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if the form is submitted
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)  # Bind form with customer data
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('customerdashboard', customer_id=customer.id)  # Redirect to dashboard or relevant page
    else:
        form = CustomerForm(instance=customer)  # Pre-populate form with existing customer data

    return render(request, 'account_management.html', {'form': form, 'customer': customer})

