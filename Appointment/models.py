from django.db import models
from Accounts.models import User
from datetime import datetime
from Accounts.models import *
# Create your models here.


slots = [
    ('9am-10am', '9am-10am'),
    ('10am-11am', '10am-11am'),
    ('11am-12pm', '11am-12pm'),
    ('12pm-1pm', '12pm-1pm'),
    ('3pm-4pm', '3pm-4pm'),
    ('4pm-5pm', '4pm-5pm'),
    ('5pm-6pm', '5pm-6pm'),
    ('6pm-7pm','6pm-7pm'),
]

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    time_slot = models.CharField(max_length=20, choices=slots)
    status=models.BooleanField(default=False)
    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time_slot}"

class Report(models.Model):
    app=models.OneToOneField(Appointment,on_delete=models.CASCADE)
    symptoms=models.TextField()
    prescription=models.TextField()
    Advice=models.TextField()
    def __str__(self):
        return f"Dr {self.app.doctor} Patient {self.app.patient}"


bedtype = [
    ('Ebed', 'Emergency'),
    ('Gbed', 'General')
]
class BedBooking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bed=models.ForeignKey(Bed, on_delete=models.CASCADE)
    bedtype=models.CharField(max_length=20, choices=bedtype)
    startdate = models.DateField(default=datetime.now)
    enddate = models.DateField(default=datetime.now)
    def __str__(self):
        return f"{self.bed.dept.dname}-{self.bedtype} from {self.startdate} to {self.enddate}"