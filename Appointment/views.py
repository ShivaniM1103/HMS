from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from Accounts.views import login_view
from .models import *
from .forms import *
from Accounts.models import User
from Accounts.views import account
from django.db.models import Q 
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.http import HttpResponse
from datetime import datetime, timedelta, time
from django.contrib import messages
from django.utils import timezone
# Create your views here.


# def doctor(request,id):
#     doc=Doctor.objects.filter(department=id)
#     return render(request ,'doctors.html', context={'doc':doc})
def doctor(request, id):
    doctors = Doctor.objects.filter(department=id)

    slots = [
        ('9am-10am', time(9, 0)),
        ('10am-11am', time(10, 0)),
        ('11am-12pm', time(11, 0)),
        ('12pm-1pm', time(12, 0)),
        ('3pm-4pm', time(15, 0)),
        ('4pm-5pm', time(16, 0)),
        ('5pm-6pm', time(17, 0)),
        ('6pm-7pm', time(18,0)),
    ]

    current_datetime = datetime.now()
    free_slots = {}

    for doctor in doctors:
        free_slot_found = False
        for day in range(30):  # Check up to 30 days ahead
            date = (current_datetime + timedelta(days=day)).date()
            for slot_name, slot_time in slots:
                slot_datetime = datetime.combine(date, slot_time)
                if slot_datetime > current_datetime:
                    if not Appointment.objects.filter(doctor=doctor, date=date, time_slot=slot_name, status=False).exists():
                        free_slots[doctor.id] = {'date': date, 'time_slot': slot_name}
                        free_slot_found = True
                        break
            if free_slot_found:
                break
        if not free_slot_found:
            free_slots[doctor.id] = {'date': None, 'time_slot': None}

    return render(request, 'doctors.html', context={'doc': doctors, 'free_slots': free_slots})

@login_required
def appointment(request, id):
    user = request.user
    doc = get_object_or_404(Doctor, pk=id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time_slot = form.cleaned_data['time_slot']
            existing_appointments = Appointment.objects.filter(doctor=doc, date=date, time_slot=time_slot, status=False).count()
            if existing_appointments > 0:
                form.add_error('time_slot', 'This time slot is already full. Please select a different one.')
            else:
                new_appointment = form.save(commit=False)
                new_appointment.patient = user.patient  # Ensure user has a related Patient object
                new_appointment.doctor = doc
                new_appointment.save()
                messages.success(request, 'Booking Successful. Check your Appointments')
                return redirect('departments')
    else:
        form = AppointmentForm()

    return render(request, 'appointment.html', context={'form': form, 'doctor': doc})

def report(request,id):
    msg=None
    app = get_object_or_404(Appointment, pk=id)
    app_details=Appointment.objects.get(pk=id)
    form = ReportForm()
    return render(request,'report.html', {'form': form, 'msg': msg,'app_details':app_details})

def reportsubmit(request):
    appid=request.POST['appid']
    app = get_object_or_404(Appointment, pk=appid)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            rep = form.save(commit=False)
            rep.app = app # Ensure user has a related Patient object
            app.status=True
            app.save()
            rep.save()
            return redirect(reportlist)
        else:
            msg = 'form is not valid'
            return redirect(appointmentlist)
    else:
        form = ReportForm()
        return redirect(appointmentlist)
    
@login_required
def reportlist(request):
    user = request.user
    if user.is_doctor:
        # Get the logged-in doctor
        doctor = request.user.doctor

        # Get the reports for this doctor, ordered by appointment date in descending order
        reports = Report.objects.filter(app__doctor=doctor).order_by('-app__date')
        context = {
            'reports': reports,
        }
        return render(request, 'reportlist.html', context)
    elif user.is_patient:
        patient = request.user.patient

        # Get the reports for this doctor, ordered by appointment date in descending order
        reports = Report.objects.filter(app__patient=patient).order_by('-app__date')
        context = {
            'reports': reports,
        }
        return render(request, 'reportlist.html', context)

@login_required
def appointmentlist(request):
    user=request.user
    if user.is_doctor:
        # Get the logged-in doctor
        doctor = request.user.doctor

        # Get the reports for this doctor, ordered by appointment date in descending order
        appointments = Appointment.objects.filter(doctor=doctor,status=False).order_by('-date','-time_slot')
        context = {
            'appointments': appointments,
        }
        return render(request, 'all_app_list.html', context)
    elif user.is_patient:
        today = timezone.now().date()
        patient = request.user.patient
        bedbookings=BedBooking.objects.filter(patient=patient).order_by('-startdate','-enddate')
        # Get the reports for this doctor, ordered by appointment date in descending order
        appointments = Appointment.objects.filter(patient=patient).order_by('-date','-time_slot')
        context = {
            'appointments': appointments,
            'bedbookings':bedbookings,
            'today':today
        }
        return render(request, 'all_app_list.html', context)
    elif user.is_superuser:
        today = timezone.now().date()
        bedbookings=BedBooking.objects.all().order_by('-startdate','-enddate')
        # Get the reports for this doctor, ordered by appointment date in descending order
        appointments = Appointment.objects.all().order_by('-date','-time_slot')
        context = {
            'appointments': appointments,
            'bedbookings':bedbookings,
            'today':today
        }
        return render(request, 'all_app_list.html', context)
    else:
        return redirect(login_view)


@login_required
def search_appointments(request):
    user = request.user
    appointments = None

    if user.is_doctor:
        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            doctor = None

        if request.method == 'POST':
            patient_name = request.POST.get('patientname', '').strip()
            if patient_name:
                # Split the patient_name to search first name and last name separately
                names = patient_name.split()
                if len(names) == 1:
                    appointments = Appointment.objects.filter(
                        Q(patient__user__first_name__icontains=names[0]) |
                        Q(patient__user__last_name__icontains=names[0]),
                        doctor=doctor,
                        status=False  # pending appointments
                    ).order_by('-date', '-time_slot')
                elif len(names) > 1:
                    appointments = Appointment.objects.filter(
                        Q(patient__user__first_name__icontains=names[0]) &
                        Q(patient__user__last_name__icontains=names[1]),
                        doctor=doctor,
                        status=False  # pending appointments
                    ).order_by('-date', '-time_slot')
                return render(request, 'all_app_list.html', {'appointments': appointments})

    if user.is_superuser:
        if request.method == 'POST':
            patient_name = request.POST.get('patientname', '').strip()
            if patient_name:
                # Split the patient_name to search first name and last name separately
                names = patient_name.split()
                if len(names) == 1:
                    appointments = Appointment.objects.filter(
                        Q(patient__user__first_name__icontains=names[0]) |
                        Q(patient__user__last_name__icontains=names[0])
                    ).order_by('-date', '-time_slot')
                    bedbookings = BedBooking.objects.filter(
                        Q(patient__user__first_name__icontains=names[0])   
                    ).order_by('-startdate', '-enddate')
                elif len(names) > 1:
                    appointments = Appointment.objects.filter(
                        Q(patient__user__first_name__icontains=names[0]) &
                        Q(patient__user__last_name__icontains=names[1])
                    ).order_by('-date', '-time_slot')
                    bedbookings = BedBooking.objects.filter(
                        Q(patient__user__first_name__icontains=names[0]) &  
                        Q(patient__user__last_name__icontains=names[0])
                    ).order_by('-startdate', '-enddate')

                return render(request, 'all_app_list.html', {'appointments': appointments,'bedbookings':bedbookings})
    return render(request, 'all_app_list.html', {'appointments': appointments,})

@login_required
def search_reports(request):
    user = request.user
    appointments = None

    if user.is_doctor:
        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            doctor = None

        if request.method == 'POST':
            patient_name = request.POST.get('patientname', '').strip()
            if patient_name:
                # Split the patient_name to search first name and last name separately
                names = patient_name.split()
                if len(names) == 1:
                    reports = Report.objects.filter(
                        Q(app__patient__user__first_name__icontains=names[0]) |
                        Q(app__patient__user__last_name__icontains=names[0]),
                        app__doctor=doctor
                    ).order_by('-app__date', '-app__time_slot')
                elif len(names) > 1:
                    reports = Report.objects.filter(
                        Q(app__patient__user__first_name__icontains=names[0]) &
                        Q(app__patient__user__last_name__icontains=names[1]),
                        app__doctor=doctor
                    ).order_by('-app__date', '-app__time_slot')
    
    return render(request, 'reportlist.html', {'reports': reports})


def medicalreport(request, id):
    report = get_object_or_404(Report, pk=id)
    appointment = report.app
    doctor = appointment.doctor
    patient = appointment.patient

    context = {
        'report': report,
        'appointment': appointment,
        'doctor': doctor,
        'patient': patient,
    }

    return render(request, 'print.html', context)




def generate_pdf(request, id):
    report = get_object_or_404(Report, pk=id)
    appointment = report.app
    doctor = appointment.doctor
    patient = appointment.patient
    # Render the HTML template
    template = get_template('print.html')
    html = template.render({'report': report, 'appointment': appointment, 'doctor': doctor, 'patient': patient})
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="medical_report.pdf"'
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response

def delapp(request,id):
    user=request.user
    Appointment.objects.get(pk=id).delete()
    messages.success(request, 'Appointment deleted')
    if user.is_superuser:
        return redirect('appointmentlist')
    return redirect('account')

def delbedbook(request,id):
    user=request.user
    BedBooking.objects.get(pk=id).delete()
    messages.success(request, 'Booking deleted')
    if user.is_superuser:
        return redirect('appointmentlist')
    return redirect('appointmentlist')

def delpending(request):
    current_date = timezone.now().date()
    # Delete appointments where the date is before the current date and status is pending
    Appointment.objects.filter(
        status=False,
        date__lt=current_date
    ).delete()
    return redirect('appointmentlist') 

@login_required
def bookbedform(request,id):
    user = request.user
    if user.is_patient:
        form = PatientBookBedForm()
        return render(request,'bookbed.html', {'form': form,'id':id})
    elif user.is_superuser:
        form = AdminBookBedForm()
        return render(request,'bookbed.html', {'form': form,'id':id})
    else:
        redirect('index')

def bookbed(request,id):
    msg=None
    department = get_object_or_404(Departments, pk=id)
    bed = get_object_or_404(Bed, dept=department)
    user = request.user
    if user.is_patient:
        if request.method == 'POST':
            form = PatientBookBedForm(request.POST)
            if form.is_valid():
                startdate = form.cleaned_data['startdate']
                enddate = form.cleaned_data['enddate']
                if (enddate - startdate).days > 5:
                    messages.success(request, 'Cannot book for more than 5 days')
                    return redirect('bookbedform',id=id)
                bedtype_choice = 'Gbed'  # Default for patients
                total_beds = bed.Gbed
                booked_beds = BedBooking.objects.filter(
                    bed=bed,
                    bedtype=bedtype_choice,
                    startdate__lte=enddate,
                    enddate__gte=startdate
                ).count()

                if booked_beds < total_beds:
                    BedBooking.objects.create(
                        patient=request.user.patient,  # Ensure this maps correctly to your patient model
                        bed=bed,
                        bedtype=bedtype_choice,
                        startdate=startdate,
                        enddate=enddate
                    )
                    messages.success(request, 'Bed booked Successfully!')
                    return redirect('departments')
                else:
                    messages.success(request, 'No bed available for these dates!')
                    return redirect('bookbedform',id=id)
        else:
            form = PatientBookBedForm()
    elif user.is_superuser:
        if request.method == 'POST':
            form = AdminBookBedForm(request.POST)
            if form.is_valid():
                startdate = form.cleaned_data['startdate']
                enddate = form.cleaned_data['enddate']
                bedtype=form.cleaned_data['bedtype']
                if (enddate - startdate).days > 5:
                    messages.success(request, 'Cannot book for more than 5 days')
                    return redirect('bookbedform',id=id)
                total_beds = getattr(bed, bedtype)
                booked_beds = BedBooking.objects.filter(
                    bed=bed,
                    bedtype=bedtype,
                    startdate__lte=enddate,
                    enddate__gte=startdate
                ).count()

                if booked_beds < total_beds:
                    b=form.save(commit=False)
                    b.bed=bed
                    b.save()
                    messages.success(request, 'Bed booked Successfully!')
                    return redirect('departments')
                else:
                    messages.success(request, 'No bed available for these dates!')
                    return redirect('bookbedform',id=id)
        else:
            form = PatientBookBedForm()
    return redirect(bookbedform)


# def appointment(request, id):
#     if request.user.is_authenticated:
#         user = request.user
#         doc = get_object_or_404(Doctor, pk=id)
        
#         if request.method == 'POST':
#             form = AppointmentForm(request.POST)
#             if form.is_valid():
#                 date = form.cleaned_data['date']
#                 time_slot = form.cleaned_data['time_slot']
#                 existing_appointments = Appointment.objects.filter(doctor=doc,date=date, time_slot=time_slot,status=False).count()
#                 if existing_appointments == 1:
#                     form.add_error('time_slot', 'This time slot is already full. Please select a different one.')
#                 else:
#                     new_appointment = form.save(commit=False)
#                     new_appointment.patient = user.patient  # Ensure user has a related Patient object
#                     new_appointment.doctor = doc
#                     new_appointment.save()
#                     return redirect('departments')
#         else:
#             form = AppointmentForm()
            
#         return render(request, 'appointment.html', context={'form': form, 'doctor': doc})
#     else:
#         return redirect(login_view)


# class generate_pdf(View):
#     def get(self, request, id, *args, **kwargs):
#         # Get the report object
#         report = get_object_or_404(Report, pk=id)

#         # Create a PDF document
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="medical_report.pdf"'

#         # Create a canvas
#         p = canvas.Canvas(response, pagesize=letter)
        
#         # Write content to the PDF
#         p.drawString(100, 750, "Medical Report")
#         p.drawString(100, 730, "Report ID: {}".format(report.id))
#         p.drawString(100, 710, "Symptoms: {}".format(report.symptoms))
#         p.drawString(100, 690, "Prescription: {}".format(report.prescription))
#         p.drawString(100, 670, "Advice: {}".format(report.Advice))
        
#         # Close the PDF
#         p.showPage()
#         p.save()

#         return response