# Generated by Django 3.1.1 on 2020-11-01 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0017_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='first',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='last',
            new_name='middlename',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='middle',
            new_name='surname',
        ),
    ]