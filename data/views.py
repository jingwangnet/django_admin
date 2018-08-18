from django.shortcuts import render
from .models import Company,Employees 
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'base.html')
    
