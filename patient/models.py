from django.contrib.auth.models import User
from django.db import models

CHOICES = [('Male', 'Male'), ('Female', 'Female')]

SUB_CITY_CHOICES = [(' ', 'Subcity'),
                    ('Addis Ketema', 'Addis Ketema'),
                    ('Akaki Kaliti', 'Akaki Kaliti'),
                    ('Arada', 'Arada'),
                    ('Bole', 'Bole'),
                    ('Gullele', 'Gullele'),
                    ('Kirkos', 'Kirkos'),
                    ('Kolfe Keranio', 'Kolfe Keranio'),
                    ('Lideta', 'Lideta'),
                    ('Nefassilk', 'Nefas Silk'),
                    ('Yeka', 'Yeka'),
                    ]


def increment_card_number():
    last_card_number = Patient.objects.all().order_by('id').last()
    if last_card_number:
        return 'CN-' + format(last_card_number.id + 1, '04d')
    else:
        return 'CN-' + format(1, '04d')


class Address(models.Model):
    kebele = models.PositiveIntegerField(blank=True, null=True)
    woreda = models.PositiveIntegerField(blank=True, null=True)
    sub_city = models.CharField(
        max_length=20, choices=SUB_CITY_CHOICES, default=None, blank=True, null=True)
    # city = models.CharField(
    #     max_length=64, default="Addis Ababa", blank=True, null=True)
    # country = models.CharField(
    #     max_length=64, default="Ethiopia", blank=True, null=True)
    # house_number = models.CharField(
    #     max_length=64, default="New", blank=True, null=True)
    # address_of = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.CASCADE, default=1, related_name="address")

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f'{self.kebele} | {self.woreda} | {self.sub_city} '


class Patient(models.Model):
    card_number = models.CharField(
        max_length=20, default=increment_card_number, editable=False)
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64, blank=True, null=True)
    middle = models.CharField(max_length=64, blank=True, null=True)
    gender = models.CharField(
        max_length=20, choices=CHOICES, default=None, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    created_date = models.DateField(auto_now_add=True)
    # appointment = models.DateField(blank=True, null=True)

    address = models.OneToOneField(Address, blank=True, null=True, on_delete=models.CASCADE,
                                   default=1, related_name="patient")

    created_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.PROTECT,
                                   related_name="creator")
    updated_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.PROTECT,
                                   related_name="editor")
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.card_number} | {self.first} | {self.last} | {self.created_date}'

    class Meta:
        ordering = ['-id']


class Doctor(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64, blank=True, null=True)
    middle = models.CharField(max_length=64, blank=True, null=True)
    specialised = models.CharField(max_length=65, blank=True, null=True)

    # created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    # updated_at = models.DateField(auto_now=True, blank=True, null=True)
    # updated_by = models.ForeignKey(
    #     User, default=None, blank=True, null=True, on_delete=models.PROTECT,  related_name="editor")
    # created_by = models.ForeignKey(
    #     User, default=None, blank=True, null=True, on_delete=models.PROTECT, related_name="creator")

    # Doctors Table


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='appointed')
    doctor = models.ForeignKey(
        Doctor, default=None, blank=True, null=True, on_delete=models.PROTECT, related_name='assigned')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.patient.first} | {self.doctor}'

    class Meta:
        ordering = ['-date']

    # Appointment table
    # Age min
    # History table/
    # dashboard
