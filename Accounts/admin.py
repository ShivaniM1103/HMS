from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Departments)
admin.site.register(Pharmacist)
admin.site.register(Bed)