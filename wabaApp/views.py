from django.shortcuts import render

# Create your views here.
def blank_page(request):
    return render(request, 'blank-page.html')

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def login_admin(request):
    return render(request, 'loginadmin.html')

def register(request):
    return render(request, 'register.html')

def customerdashboard(request):
    return render(request, 'dashboard-customer.html')
