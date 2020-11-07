from .models import Appointment, Patient, Doctor
import datetime

def base_context(request):
    return {
        "base_patient_count": Patient.objects.all().count(),
        "base_patient_today_count": Patient.objects.filter(created_date=datetime.date.today()).count(),
        'base_appointment_today_count': Appointment.objects.filter(date=datetime.date.today()).count(),
        'base_appointment_tomorrow_count': Appointment.objects.filter(date=datetime.date.today() + datetime.timedelta(days=1)).count(),
        "base_doctor_count": Doctor.objects.all().count(),
    }