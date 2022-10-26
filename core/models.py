from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Gender


class Counties(models.TextChoices):
    MOMBASA = "Mombasa", _('Mombasa')
    KWALE = "Kwale", _('Kwale')
    KILIFI = "Kilifi", _('Kilifi')
    TANA_RIVER = "Tana_River", _('Tana_River')
    LAMU = "Lamu", _('Lamu')
    TAITA_TAVETA = "Taita_Taveta", _('Taita_Taveta')
    GARISSA = "Garissa", _('Garissa')
    WAJIR = "Wajir", _('Wajir')
    MANDERA = "Mandera", _('Mandera')
    MARSABIT = "Marsabit", _('Marsabit')
    ISIOLO = "Isiolo", _('Isiolo')
    MERU = "Meru", _('Meru')
    THARAKA_NITHI = "Tharaka_Nithi", _('Tharaka_Nithi')
    EMBU = "Embu", _('Embu')
    KITUI = "Kitui", _('Kitui')
    MACHAKOS = "Machakos", _('Machakos')
    MAKUENI = "Makueni", _('Makueni')
    NYANDARUA = "Nyandarua", _('Nyandarua')
    NYERI = "Nyeri", _('Nyeri')
    KIRINYAGA = "Kirinyaga", _('Kirinyaga')
    MURANGA = "Muranga", _('Muranga')
    KIAMBU = "Kiambu", _('Kiambu')
    TURKANA = "Turkana", _('Turkana')
    WEST_POKOT = "West_Pokot", _('West_Pokot')
    SAMBURU = "Samburu", _('Samburu')
    TRANS_NZOIA = "Trans_Nzoia", _('Trans_Nzoia')
    UASIN_GISHU = "Uasin_Gishu", _('Uasin_Gishu')
    ELGEY_MARAKWET = "Elgey_Marakwet", _('Elgey_Marakwet')
    NANDI = "Nandi", _('Nandi')
    BARINGO = "Baringo", _('Baringo')
    LAIKIPIA = "Laikipia", _('Laikipia')
    NAKURU = "Nakuru", _('Nakuru')
    NAROK = "Narok", _('Narok')
    KAJIADO = "Kajiado", _('Kajiado')
    KERICHO = "Kericho", _('Kericho')
    BOMET = "Bomet", _('Bomet')
    KAKAMEGA = "Kakamega", _('Kakamega')
    VIHIGA = "Vihiga", _('Vihiga')
    BUNGOMA = "Bungoma", _('Bungoma')
    BUSIA = "Busia", _('Busia')
    SIAYA = "Siaya", _('Siaya')
    KISUMU = "Kisumu", _('Kisumu')
    HOMA_BAY = "Homa_Bay", _('Homa_Bay')
    MIGORI = "Migori", _('Migori')
    KISII = "Kisii", _('Kisii')
    NYAMIRA = "Nyamira", _('Nyamira')
    NAIROBI = "Nairobi", _('Nairobi')


class OffenceCategory(models.TextChoices):
    Stalking = 'Stalking', _('Stalking')
    SexualViolence = 'Sexual Violence', _('Sexual Violence')
    PhysicalViolence = 'Physical Violence', _('Physical Violence')
    EmotionalViolence = 'Emotional Violence', _('Emotional Violence')
    HarmfulTraditionalPractices = 'Harmful Traditional Practices', _('Harmful Traditional Practices')
    Other = 'Other', _('Other')


class Relationship(models.TextChoices):
    Spouse = "Spouse", _('Spouse')
    Friend = "Friend", _('Friend')
    Relative = "Relative", _('Relative')
    Stranger = "Stranger", _('Stranger')


class Incident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offence_category = models.CharField(max_length=150, choices=OffenceCategory.choices)
    date_of_incident = models.DateTimeField()
    country_of_incident = models.CharField(max_length=100, choices=Counties.choices)
    location_of_incident = models.CharField(max_length=150, blank=True, null=True, default=None)
    perpetrator_name = models.CharField(max_length=150)
    perpetrator_phone_number = models.CharField(max_length=50)
    perpetrator_gender = models.CharField(max_length=20, choices=Gender.choices)
    relationship_to_perpetrator = models.CharField(max_length=100, choices=Relationship.choices)
    perpetrator_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        if self.pk:
            return f'{self.user.username} crime({self.pk})'
        return super(Incident, self).__str__()
