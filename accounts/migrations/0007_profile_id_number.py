# Generated by Django 4.1.2 on 2022-11-21 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_number',
            field=models.CharField(default=1020304, max_length=50),
            preserve_default=False,
        ),
    ]