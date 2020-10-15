from django import forms
from datetime import datetime, timedelta
from .models import CHOICES, SUB_CITY_CHOICES, Address, Patient, Appointment
from django.forms.fields import Field
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper


class DateInput(forms.DateInput):
    input_type = 'date'


class AddressForm(forms.ModelForm):
    kebele = forms.CharField(label="Kebele", required=False)
    woreda = forms.CharField(label="Woreda", required=False)
    sub_city = forms.ChoiceField(
        label="Subcity", choices=SUB_CITY_CHOICES, required=False)

    class Meta:
        model = Address
        fields = ['kebele', 'woreda', 'sub_city']


class PatientForm(forms.ModelForm):
    first = forms.CharField(label="First Name")
    sur = forms.CharField(label="Sur Name", required=False)
    middle = forms.CharField(label="Middle Name", required=False)
    gender = forms.ChoiceField(
        choices=CHOICES, required=False)
    # widget=forms.RadioSelect,
    age = forms.IntegerField(label="Age", required=False)
    phone = forms.IntegerField(label="Phone", required=False)
    appointment = forms.DateField(
        label="Appointment",
        widget=DateInput(
            attrs={
                "min": datetime.now().date().strftime("%Y-%m-%d")
            }),
        required=False
    )

    class Meta:
        model = Patient
        fields = ['first', 'sur', 'middle',
                  'gender', 'age', 'phone', 'appointment']


class AppointmentForm(forms.ModelForm):
    # patient = forms.CharField(label="First Name")

    date = forms.DateField(
        label="Appointment",
        widget=DateInput(
            attrs={
                "min": datetime.now().date().strftime("%Y-%m-%d")
            }),
        required=False
    )

    class Meta:
        model = Appointment
        fields = ['date', 'doctor', 'time']
