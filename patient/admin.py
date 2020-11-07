from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from .models import Patient, Doctor, Appointment, History

admin.site.site_header = 'Dr. Haile Y/Berhane Internal Medicine Speciality Clinic'
admin.site.site_title = 'Clinic Management System'
admin.site.index_title = 'Clinic Management System'
admin.empty_value_display = '**Empty**'


class PatientAdmin(ImportExportModelAdmin):
    list_display = ('card_number', 'firstname', 'surname', 'created_date')
    list_per_page = 20
    search_fields = ('card_number', 'firstname', 'surname', 'middlename', 'created_date', 'appointment', 'phone', 'gender')
    list_filter = ('gender', 'created_date')


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(History)

admin.site.unregister(Group)
