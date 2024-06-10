
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import authenticate, login,logout
from Appointment.models import *
from datetime import date
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form but don't commit to the database yet
            user.is_patient = True  # Set the is_patient field to True
            user.save()  # Now save the user to the database           
            msg = 'User created'
            return redirect('login_view')
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

def staff_reg(request):
    msg = None
    if request.method == 'POST':
        form = StaffSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('staff_reg')
        else:
            msg = 'form is not valid'
    else:
        form = StaffSignUpForm()
    return render(request,'staff_reg.html', {'form': form, 'msg': msg})

def departments(request):
    if request.user.is_authenticated:
        depts=Departments.objects.all().order_by('id')
        return render(request ,'departments.html', context={'depts':depts})
    else:
        return redirect(login_view)

def search_department(request):
    if request.method == 'POST':
        query = request.POST.get('searchdept')
        # departments = Departments.objects.none()
        if query:
            departments = Departments.objects.filter(dname__icontains=query)
        else:
            departments = Departments.objects.all().order_by('id')
    else:
        departments = Departments.objects.all().order_by('id')
    
    return render(request, 'departments.html',context={'depts': departments})

# def search_doctor(request):
#     if request.method == 'POST':
#         query = request.POST.get('searchdoc')
#         # departments = Departments.objects.none()
#         if query:
#             doctors = Doctor.objects.filter(user__username__icontains=query)
#         else:
#             doctors = Doctor.objects.all().order_by('user__id')
#     else:
#         doctors = Doctor.objects.all().order_by('user__id')
    
#     return render(request, 'doctors.html', context={'doctors': doctors})

def adddept(request):
    msg = None
    if request.method == 'POST':
        form = DepartmentsForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Department created Successfully!')
            return redirect(departments)
        else:
            messages.success(request, 'Form not valid!')
    else:
        form = DepartmentsForm()
    return render(request,'add_dept_form.html', {'form': form, 'msg': msg})

def addbed(request,id):
    msg = None
    dept = get_object_or_404(Departments, pk=id)
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            existing = Bed.objects.filter(dept=dept)
            if existing:
                Ebed = form.cleaned_data['Ebed']
                Gbed = form.cleaned_data['Gbed']
                b=Bed.objects.get(dept=dept)
                b.Ebed+=Ebed
                b.Gbed+=Gbed
                b.save()
                messages.success(request, 'Beds added Successfully!')
                return redirect(departments)
            bed = form.save(commit=False)
            bed.dept=dept
            bed.save()
            messages.success(request, 'Beds added Successfully!')
            return redirect(departments)
        else:
            messages.success(request, 'Form not valid!')
    else:
        form = BedForm()
    return render(request,'addbed.html', {'form': form, 'msg': msg})

def addbedform(request,id):
    form = BedForm()
    return render(request,'addbed.html', {'form': form, 'id': id})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('account')
            else:
                messages.success(request, 'Incorrect values')
        else:
            messages.success(request, 'Invalid form')
    return render(request, 'login.html', {'form': form})

def account(request):
    if request.user.is_authenticated:
        user = request.user
        today=date.today()
        if user.is_patient:
            try:
                details = Patient.objects.get(user=user)
            except Patient.DoesNotExist:
                details = None
            if details:
                existing_appointments = Appointment.objects.filter(patient=user.patient,status=False).order_by('-date', '-time_slot')
                if not existing_appointments:
                    existing_appointments=None
                return render(request, 'account.html', context={'details': details,'appointments': existing_appointments})
            else:
                existing_appointments=None
                form = PatientProfileForm()
                return render(request, 'account.html', context={'details': details,'appointments': existing_appointments, 'form': form})
        
        if user.is_doctor:
            try:
                details = Doctor.objects.get(user=user)
            except Doctor.DoesNotExist:
                details = None
            if details:
                
                existing_appointments = Appointment.objects.filter(doctor=user.doctor,status=False,date=today).order_by('-date', '-time_slot')
                if not existing_appointments:
                    existing_appointments=None
                return render(request, 'account.html', context={'details': details,'appointments': existing_appointments})
            else:
                existing_appointments=None
                form = DoctorProfileForm()
                return render(request, 'account.html', context={'details': details,'appointments': existing_appointments, 'form': form})
        
        if user.is_pharmacist:
            try:
                details = Pharmacist.objects.get(user=user)
            except Pharmacist.DoesNotExist:
                details = None
            if details:
                return render(request, 'account.html', context={'details': details})
            else:
                form = PharmacistProfileForm()
                return render(request, 'account.html', context={'details': details, 'form': form})
        if user.is_superuser:
            details = user
            return render(request, 'account.html', context={'details': details})
    else:       
        return redirect(login_view) 

def complete_profile(request):
    if request.user.is_authenticated:
        user = request.user 
        if user.is_patient:
            if request.method == 'POST':
                form = PatientProfileForm(request.POST,request.FILES)
                if form.is_valid():
                    patient_profile=form.save(commit=False)
                    patient_profile.user=user
                    patient_profile.save()
                    return redirect('account')
                else:
                    msg = 'form is not valid'
            else:
                form = PatientProfileForm()
        elif user.is_doctor:
            if request.method == 'POST':
                form = DoctorProfileForm(request.POST, request.FILES)
                if form.is_valid():
                    doctor_profile = form.save(commit=False)
                    doctor_profile.user = user
                    doctor_profile.save()
                    department = doctor_profile.department
                    department.No_of_doctors += 1
                    department.save()
                    return redirect('account')  # Redirect to the account view
                else:
                    return render(request, 'account.html', {'form': form})
            else:
                form = DoctorProfileForm()
                return render(request, 'account.html', {'form': form})
    
    return redirect('account') 


def change_doc_status(request, id):
    doc = get_object_or_404(Doctor, pk=id)
    doc.status = not doc.status  # Toggle the status
    doc.save()
    return redirect('account') 
# def account(request):
#     if request.user.is_authenticated:
#         user = request.user
#         if user.is_patient:
#             try:
#                 details = Patient.objects.get(user=user)
#             except Patient.DoesNotExist:
#                 details = None
#             if request.method == 'POST':
#                 form = PatientProfileForm(request.POST, request.FILES, instance=details)
#                 if form.is_valid():
#                     form.save()
#                     return redirect('account')  # Redirect to the same page to see the updated profile
#             else:
#                 form = PatientProfileForm(instance=details)

#             existing_appointments = Appointment.objects.filter(patient=user.patient).order_by('-date', '-time_slot') if details else None

#             if not existing_appointments or not existing_appointments.exists():
#                 msg = 'No appointments'
#                 return render(request, 'account.html', context={'msg': msg, 'details': details, 'form': form})
#             else:
#                 return render(request, 'account.html', context={'appointments': existing_appointments, 'details': details, 'form': form})
#         elif user.is_doctor:
#             try:
#                 doctor_instance = user.doctor
#                 details = doctor_instance
#             except Doctor.DoesNotExist:
#                 details = None
#             if details:
#                 doc_appointments = Appointment.objects.filter(doctor=doctor_instance).order_by('-date', '-time_slot')
#                 if not doc_appointments.exists():
#                     msg = 'No appointments'
#                     return render(request, 'account.html', context={'msg': msg, 'details': details})
#                 else:
#                     return render(request, 'account.html', context={'appointments': doc_appointments, 'details': details})
#             else:
#                 form=DoctorProfileForm(instance=details)
#                 return render(request, 'account.html', context={'msg': 'You are not registered as a doctor yet.','form':form})
#         elif user.is_pharmacist:
#             try:
#                 Pharmacist_instance = user.pharmacist
#                 details = Pharmacist_instance
#             except Pharmacist.DoesNotExist:
#                 details = None
#             if details:
#             #details = Pharmacist.objects.get(user=user)
#                 return render(request, 'account.html', context={'details': details})
#             else:
#                 form=PharmacistProfileForm(instance=details)
#                 return render(request, 'account.html', context={'msg': 'You are not registered as a pharmacist yet.','form':form})
#         elif user.is_superuser:
#             details = user
#             return render(request, 'account.html', context={'details': details})
#     else:
#         return redirect(login_view)


# @login_required
# def complete_profile(request):
#     user = request.user
#     if user.is_patient:
#         if not hasattr(user, 'patient'):
#             patient = Patient(user=user)
#         else:
#             patient = user.patient

#         if request.method == 'POST':
#             form = PatientProfileForm(request.POST, request.FILES, instance=patient)
#             if form.is_valid():
#                 temp=form['profile_pic'].value()
#                 if temp==None:
#                     print('null')
#                 form.save()
#                 return redirect('account')  # Redirect to account page after saving
#         else:
#             form = PatientProfileForm(instance=patient)

#         context = {
#             'form': form,
#             'details': patient,
#         }
#     elif user.is_doctor:
#         if not hasattr(user, 'doctor'):
#             doctor = Doctor(user=user)
#         else:
#             doctor = user.doctor

#         if request.method == 'POST':
#             form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
#             if form.is_valid():
#                 form.save()
#                 return redirect('account')  # Redirect to account page after saving
#         else:
#             form = DoctorProfileForm(instance=doctor)

#         context = {
#             'form': form,
#             'details': doctor,
#         }
#     elif user.is_pharmacist:
#         if not hasattr(user, 'pharmacist'):
#             pharmacist = Pharmacist(user=user)
#         else:
#             pharmacist = user.pharmacist

#         if request.method == 'POST':
#             form = PharmacistProfileForm(request.POST, request.FILES, instance=pharmacist)
#             if form.is_valid():
#                 form.save()
#                 return redirect('account')  # Redirect to account page after saving
#         else:
#             form = PharmacistProfileForm(instance=pharmacist)

#         context = {
#             'form': form,
#             'details': pharmacist,
#         }    
#     return render(request, 'account.html', context)


def signout(request):
    logout(request)
    return redirect('login_view')