# Generated by Django 4.1.2 on 2022-11-20 15:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_alter_incidentevent_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='police',
            field=models.ManyToManyField(related_name='police', to=settings.AUTH_USER_MODEL),
        ),
    ]
