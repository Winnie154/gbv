from django import forms

from core.models import Incident


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = '__all__'
        exclude = 'user',
