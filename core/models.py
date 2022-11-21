from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Gender


class Counties(models.TextChoices):
    MOMBASA = "Mombasa", _('Mombasa')
    UASIN_GISHU = "Uasin_Gishu", _('Uasin_Gishu')
    NAKURU = "Nakuru", _('Nakuru')
    KISUMU = "Kisumu", _('Kisumu')
    MIGORI = "Migori", _('Migori')
    KISII = "Kisii", _('Kisii')
    NAIROBI = "Nairobi", _('Nairobi')


class OffenceCategory(models.TextChoices):
    Stalking = 'Stalking', _('Stalking')
    SexualViolence = 'Sexual Violence', _('Sexual Violence')
    PhysicalViolence = 'Physical Violence', _('Physical Violence')
    EmotionalViolence = 'Emotional Violence', _('Emotional Violence')
    HarmfulTraditionalPractices = 'Harmful Traditional Practices', _('Harmful Traditional Practices')
    Other = 'Other', _('Other')


class IncidentEventType(models.TextChoices):
    PENDING = 'Pending'
    POLICE_ADDED = 'Police Added'
    INVESTIGATION_STARTED = 'Investigation Started'
    CASE_IN_COURT = 'Case In Court'
    CASE_CLOSED = 'Case Closed'
    POLICE_REMOVED = 'Police Removed'
    STATION_ASSIGNED = 'Assigned To Police Station'


class Relationship(models.TextChoices):
    Spouse = "Spouse", _('Spouse')
    Friend = "Friend", _('Friend')
    Relative = "Relative", _('Relative')
    Stranger = "Stranger", _('Stranger')


class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    ocs = models.ForeignKey(User, related_name='ocs', on_delete=models.CASCADE)
    police = models.ManyToManyField(User, related_name='officers', blank=True)
    county = models.TextField(max_length=100, choices=Counties.choices)

    def __str__(self):
        return f'{self.name} station'


class Incident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offence_category = models.CharField(max_length=150, choices=OffenceCategory.choices)
    date_of_incident = models.DateTimeField()
    county_of_incident = models.CharField(max_length=100, choices=Counties.choices)
    location_of_incident = models.CharField(max_length=150, blank=True, null=True, default=None)
    perpetrator_name = models.CharField(max_length=150)
    perpetrator_phone_number = models.CharField(max_length=50)
    perpetrator_gender = models.CharField(max_length=20, choices=Gender.choices)
    relationship_to_perpetrator = models.CharField(max_length=100, choices=Relationship.choices)
    perpetrator_image = models.ImageField(blank=True, null=True)

    police = models.ManyToManyField(to=User, related_name='police', blank=True)
    station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        if self.pk:
            return f'{self.user.username} crime({self.pk})'
        return super(Incident, self).__str__()


class IncidentEvent(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    type = models.CharField(max_length=150, choices=IncidentEventType.choices)
    desc = models.TextField()
    event_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
