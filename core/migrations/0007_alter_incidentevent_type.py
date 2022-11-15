# Generated by Django 4.1.2 on 2022-11-15 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_incident_police_alter_incidentevent_event_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentevent',
            name='type',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Police Added', 'Police Added'), ('Investigation Started', 'Investigation Started'), ('Case In Court', 'Case In Court'), ('Case Closed', 'Case Closed'), ('Police Removed', 'Police Removed')], max_length=150),
        ),
    ]