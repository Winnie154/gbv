from django import forms


class IncidentForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
