from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('signout/',views.signout,name='signout'),
    path('staff_reg/',views.staff_reg,name='staff_reg'),
    path('departments/',views.departments,name='departments'),
    path('search_department/',views.search_department,name='search_department'),
    path('adddept/',views.adddept,name='adddept'),
    path('addbedform/<int:id>',views.addbedform, name='addbedform'),
    path('addbed/<int:id>',views.addbed, name='addbed'),
    path('account/',views.account,name='account'),
    path('complete_profile/',views.complete_profile,name='complete_profile'),
    path('change_doc_status/<int:id>',views.change_doc_status,name='change_doc_status'),
]