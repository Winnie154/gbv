from django.urls import path

from core.views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('cases/', cases_views, name='cases'),
    path('police/', police_dashboard, name='police-dashboard'),
    path('case/<int:incident_id>/details/', case_details, name='case-details'),
    path('admin/', admin_dashboard, name='admin-dashboard'),
    path('admin/case/<int:incident_id>/details/', admin_case_details, name='admin-case-details'),
    path('admin/case/<int:incident_id>/add-police/', add_police_to_case, name='admin-add-police'),
    path('admin/case/<int:incident_id>/remove-police/', remove_police, name='admin-remove-police'),
    path('admin/create-police/', create_police, name='create-police'),

    path('ipoa/', ipoa_dashboard_view, name='ipoa-dashboard'),
    path('ipoa/case/<int:incident_id>/details/', ipoa_case_details_view, name='ipoa-case-details'),
    path('ipoa/case/<int:incident_id>/assign/', ipoa_case_assign_view, name='ipoa-assign'),
    path('ipoa/download-report', cases_report_view, name='download-report'),

]
