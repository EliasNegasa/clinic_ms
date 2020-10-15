# Generated by Django 3.1.1 on 2020-10-02 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import patient.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kebele', models.PositiveIntegerField(blank=True, null=True)),
                ('woreda', models.PositiveIntegerField(blank=True, null=True)),
                ('sub_city', models.CharField(blank=True, max_length=64, null=True)),
                ('city', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(default=patient.models.increment_card_number, editable=False, max_length=20)),
                ('first', models.CharField(max_length=64)),
                ('last', models.CharField(blank=True, max_length=64, null=True)),
                ('middle', models.CharField(blank=True, max_length=64, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default=None, max_length=20, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('appointment', models.DateField(blank=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='patient.address')),
                ('created_by', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='editor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
