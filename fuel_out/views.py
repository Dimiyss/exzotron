from django.shortcuts import render
from .models import FuelReports

# Create your views here.

def post_list(request):
    posts = FuelReports.objects.order_by('fuel_data')
    return render(request, 'fuel_out/post_list.html', {'posts': posts})

def main(request):
    posts = FuelReports.objects.all()
    return render(request, 'fuel_out/report.html', {'posts': posts})