from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm
from django.forms.widgets import DateInput
from datetime import datetime, time

# class AppointmentForm(ModelForm,forms.Form):
#     class Meta:
#         model=Appointment
#         fields=['date','time_slot']
#         widgets = {
#             'date': DateInput(attrs={'type': 'date'}),
#         }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        if date and date < datetime.now().date():
            self.add_error('date', 'Appointment date cannot be in the past.')

        current_time = datetime.now().time()
        slot_start_time = datetime.strptime(time_slot.split('-')[0], '%I%p').time()
        
        if date == datetime.now().date() and slot_start_time <= current_time:
            self.add_error('time_slot', 'Appointment time slot cannot be in the past.')

        return cleaned_data

class ReportForm(ModelForm,forms.Form):
    class Meta:
        model=Report
        fields=['symptoms','prescription','Advice']

class PatientBookBedForm(ModelForm,forms.Form):
    class Meta:
        model=BedBooking
        fields=['startdate','enddate']
        widgets = {
            'startdate': DateInput(attrs={'type': 'date'}),
            'enddate': DateInput(attrs={'type': 'date'}),
        }

class AdminBookBedForm(ModelForm,forms.Form):
    class Meta:
        model=BedBooking
        fields=['patient','bedtype','startdate','enddate']
        widgets = {
            'startdate': DateInput(attrs={'type': 'date'}),
            'enddate': DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'bedtype': 'Choose Bed Type',
            'startdate': 'Start Date',
            'enddate': 'End Date',
        }