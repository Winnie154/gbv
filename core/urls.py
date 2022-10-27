from django.urls import path

from core.views import dashboard, cases_views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('cases/', cases_views, name='cases')
]
