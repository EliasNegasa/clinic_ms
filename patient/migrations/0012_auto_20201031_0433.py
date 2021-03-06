# Generated by Django 3.1.1 on 2020-10-31 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_auto_20201013_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='address',
        ),
        migrations.AddField(
            model_name='patient',
            name='kebele',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='sub_city',
            field=models.CharField(blank=True, choices=[(' ', 'Subcity'), ('Addis Ketema', 'Addis Ketema'), ('Akaki Kaliti', 'Akaki Kaliti'), ('Arada', 'Arada'), ('Bole', 'Bole'), ('Gullele', 'Gullele'), ('Kirkos', 'Kirkos'), ('Kolfe Keranio', 'Kolfe Keranio'), ('Lideta', 'Lideta'), ('Nefassilk', 'Nefas Silk'), ('Yeka', 'Yeka')], default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='woreda',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
