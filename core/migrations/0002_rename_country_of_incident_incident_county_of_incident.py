# Generated by Django 4.1.2 on 2022-10-27 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='country_of_incident',
            new_name='county_of_incident',
        ),
    ]
