from django.urls import path

from core.views import dashboard, cases_views, police_dashboard, case_details

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('cases/', cases_views, name='cases'),
    path('police/', police_dashboard, name='police-dashboard'),
    path('case/<int:incident_id>/details/', case_details, name='case-details'),
]
