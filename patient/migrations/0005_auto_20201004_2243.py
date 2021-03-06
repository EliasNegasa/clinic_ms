# Generated by Django 3.1.1 on 2020-10-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20201003_1943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.AddField(
            model_name='address',
            name='house_number',
            field=models.CharField(blank=True, default='New', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='sub_city',
            field=models.CharField(blank=True, choices=[(' ', 'Subcity'), ('Addis Ketema', 'Addis Ketema'), ('Akaki Kaliti', 'Akaki Kaliti'), ('Arada', 'Arada'), ('Bole', 'Bole'), ('Gullele', 'Gullele'), ('Kirkos', 'Kirkos'), ('Kolfe Keranio', 'Kolfe Keranio'), ('Lideta', 'Lideta'), ('Nefassilk', 'Nefas Silk'), ('Yeka', 'Yeka')], default=None, max_length=20, null=True),
        ),
    ]
