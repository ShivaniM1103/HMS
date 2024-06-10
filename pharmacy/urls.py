from django.urls import path
from . import views

urlpatterns = [
    path('medlist/',views.medlist,name='medlist'),
    path('addmedform/',views.addmedform,name='addmedform'),
    path('addmed/',views.addmed,name='addmed'),
    path('meddel/<int:id>',views.meddel,name='meddel'),
    path('searchmed',views.searchmed,name='searchmed'),
    path('get_exp_meds',views.get_exp_meds,name='get_exp_meds'),
]