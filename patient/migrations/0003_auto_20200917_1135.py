# Generated by Django 3.1.1 on 2020-09-17 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_auto_20200906_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='appointment',
            field=models.DateField(blank=True, null=True),
        ),
    ]