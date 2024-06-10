from django.urls import path
from . import views
from .views import generate_pdf

urlpatterns = [
    
    path('doctor/<int:id>/', views.doctor ,name='doctor'),
    path('appointment',views.appointment,name='appointment'),
    path('appointment/<int:id>/', views.appointment ,name='appointment'),
    path('delapp/<int:id>',views.delapp,name='delapp'),
    path('report/<int:id>/', views.report ,name='report'),
    path('reportsubmit/',views.reportsubmit,name='reportsubmit'),
    path('reportlist/',views.reportlist,name='reportlist'),
    path('appointmentlist/',views.appointmentlist,name='appointmentlist'),
    path('search_appointments/',views.search_appointments,name='search_appointments'),
    path('search_reports/',views.search_reports,name='search_reports'),
    path('medicalreport/<int:id>/', views.medicalreport, name='medicalreport'),
    path('generate_pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
    path('bookbedform/<int:id>',views.bookbedform,name='bookbedform'),
    path('bookbed/<int:id>',views.bookbed,name='bookbed'),
    path('delbedbook/<int:id>',views.delbedbook,name='delbedbook'),
    path('delpending',views.delpending,name='delpending'),
]