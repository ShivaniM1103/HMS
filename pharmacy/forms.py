from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm
from django.forms.widgets import DateInput

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'manufacturer','price','manufacturer','description','quantity','expiry_date']
        labels = {
            'name': 'Medicine name',
            'manufacturer': 'Manufacturer',
            'price': 'Price',
            'description':'Description',
            'quantity':'Quantity',
            'expiry_date':'Expiry Date',
        }
        widgets = {
            'expiry_date': DateInput(attrs={'type': 'date'}),
        }