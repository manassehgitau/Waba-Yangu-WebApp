from django.shortcuts import render

# Create your views here.
def blank_page(request):
    return render(request, 'blank-page.html')

def index(request):
    return render(request, 'index.html')