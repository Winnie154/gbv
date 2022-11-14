from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Incident, IncidentEvent, IncidentEventType


@receiver(post_save, sender=Incident)
def update_incident_on_event(sender, instance: Incident, created, **kwargs):
    if created:
        event = IncidentEvent()
        event.incident = instance
        event.type = IncidentEventType.PENDING
        event.desc = 'Event created, waiting to be assigned'
        event.save()
