from django.contrib import admin

from core.models import Incident, PoliceStation, IncidentEvent

admin.site.register(Incident)
admin.site.register(PoliceStation)
admin.site.register(IncidentEvent)
