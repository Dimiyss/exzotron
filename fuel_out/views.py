from django.shortcuts import render, get_object_or_404
from .models import FuelReports
from .models import FuelOut
from django.utils import timezone
# Create your views here.

def day_report(request,pk):

    #posts = FuelReports.objects.all().exclude(fuel_out_end__lte=pk).filter(fuel_out_start__lte=pk))
    return render(request, 'fuel_out/days_report.html.html', {'posts': posts})

def main(request):
    #posts = FuelReports.objects.all()
    posts_time = FuelReports.objects.order_by('fuel_data')
    return render(request, 'fuel_out/report.html', {'posts': posts_time})