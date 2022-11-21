# Generated by Django 4.1.2 on 2022-11-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('User', 'User'), ('Police', 'Police'), ('Admin', 'Admin'), ('OCS', 'Ocs')], default='User', max_length=30),
        ),
    ]
