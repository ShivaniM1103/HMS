from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
# Create your views here.


def medlist(request):
    details = Medicine.objects.all()
    return render(request, 'medlist.html',{'details':details})

def addmedform(request):
    form=MedicineForm()
    return render(request, 'addmedform.html',{'form':form})

def addmed(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'Medicine added'
            return redirect(addmedform)
        else:
            msg = 'form is not valid'
    else:
        form = MedicineForm()
    return redirect(medlist)

def meddel(request,id):
    Medicine.objects.get(pk=id).delete()
    return redirect('medlist')


def searchmed(request):
    if request.method == 'POST':
        query = request.POST['medname']
        results = Medicine.objects.filter(name__icontains=query)
        return render(request, 'medlist.html', {'details': results})
    else:
        redirect(medlist)

def get_exp_meds(request):
    today = timezone.now().date()
    near_expiry_date = today + timedelta(days=100)  # Adjust the number of days as needed
    expiring_soon = Medicine.objects.filter(expiry_date__lte=near_expiry_date, expiry_date__gte=today)
    expired = Medicine.objects.filter(expiry_date__lt=today)
    
    context = {
        'details': list(expiring_soon) + list(expired),
        'today': today,
    }
    return render(request, 'medlist.html', context)