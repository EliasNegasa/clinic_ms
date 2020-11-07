from django import forms
from datetime import datetime, timedelta
from .models import CHOICES, SUB_CITY_CHOICES, Patient, Appointment, History, Doctor
from django.forms.fields import Field
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name")
    surname = forms.CharField(label="Sur Name", required=False)
    middlename = forms.CharField(label="Middle Name", required=False)
    gender = forms.ChoiceField(choices=CHOICES, required=False)
    age = forms.FloatField(label="Age", required=False)
    phone = forms.IntegerField(label="Phone", required=False)

    kebele = forms.IntegerField(label="Kebele", required=False)
    woreda = forms.IntegerField(label="Woreda", required=False)
    sub_city = forms.ChoiceField(label="Subcity",
                                 choices=SUB_CITY_CHOICES,
                                 required=False)

    class Meta:
        model = Patient
        fields = [
            'firstname', 'surname', 'middlename', 'gender', 'age', 'phone',
            'kebele', 'woreda', 'sub_city'
        ]

    def clean(self):
        super(PatientForm, self).clean()

        age = self.cleaned_data.get('age')
        kebele = self.cleaned_data.get('kebele')
        woreda = self.cleaned_data.get('woreda')
        phone = self.cleaned_data.get('phone')

        if age != None and age < 0:
            self._errors['age'] = self.error_class(['Minimum Age must be 0'])
        if kebele != None and kebele < 1:
            self._errors['kebele'] = self.error_class(
                ['Kebele must be greater than 1'])
        if woreda != None and woreda < 1:
            self._errors['woreda'] = self.error_class(
                ['Woreda must be greater than 1'])

        if phone != None and phone < 1:
            self._errors['phone'] = self.error_class(
                ['Phone Number is not valid'])


class HistoryForm(forms.ModelForm):
    history = forms.CharField(label="History and Physical Examination",
                              required=False,
                              widget=forms.Textarea(attrs={
                                  'rows': 5,
                                  'cols': 40
                              }))
    doctor = forms.ChoiceField(
        label="Doctor",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = History
        fields = ['history']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].choices = [(doctor.id,
                                          f'{doctor.firstname} {doctor.surname}')
                                         for doctor in Doctor.objects.all()]


class AppointmentForm(forms.ModelForm):
    # patient = forms.CharField(label="First Name")

    date = forms.DateField(
        label="Appointment",
        widget=DateInput(
            attrs={"min": datetime.now().date().strftime("%Y-%m-%d"), 'id':'assignedDoctor'}),
        required=False)

    class Meta:
        model = Appointment
        fields = ['date', 'doctor']


class DoctorForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name")
    surname = forms.CharField(label="Sur Name", required=False)
    middlename = forms.CharField(label="Middle Name", required=False)
    specialised = forms.CharField(label="Specialised in", required=False)

    phone = forms.IntegerField(label="Phone", required=False)


    class Meta:
        model = Doctor
        fields = [
            'firstname', 'surname', 'middlename', 'phone', 'specialised'
        ]

    # appointment = forms.DateField(
    #     label="Appointment",
    #     widget=DateInput(
    #         attrs={"min": datetime.now().date().strftime("%Y-%m-%d")}),
    #     required=False)