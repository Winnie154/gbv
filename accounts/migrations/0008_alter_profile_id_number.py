# Generated by Django 4.1.2 on 2022-11-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_id_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
