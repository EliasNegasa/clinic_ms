from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from .models import Patient

admin.site.site_header = 'Clinic Management System'
admin.site.site_title = 'Clinic Management System'
admin.site.index_title = 'Clinic Management System'
admin.empty_value_display = '**Empty**'


class PatientAdmin(ImportExportModelAdmin):
    list_display = ('card_number', 'first', 'last', 'created_date')
    list_per_page = 20
    search_fields = ('card_number', 'first', 'last', 'middle', 'created_date', 'appointment', 'phone', 'gender')
    list_filter = ('gender', 'created_date')


admin.site.register(Patient, PatientAdmin)

admin.site.unregister(Group)
