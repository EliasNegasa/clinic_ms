from django.urls import path
from . import views, views_doc

app_name = "patient"

urlpatterns = [
    path('', views.index, name="index"),
    # path('list', views.patient_list, name="list"),
    path('list/', views.PatientListView.as_view(), name="patient_list"),
    path('search', views.search, name="search"),
    # path('detail/<int:pk>', views.PatientDetailView.as_view(), name="patient_detail"),
    path('patients/detail/<int:patient_id>', views.patient_detail, name="patient_detail"),
    path('patients/add', views.patient_create, name="add"),
    path('patients/update/<int:patient_id>', views.patient_update, name="update"),
    path('patients/history/<int:patient_id>', views.patient_history, name="history"),
    # path('patients/update/<int:pk>', views.PatientUpdateView.as_view(), name="update"),
    path('patients/delete/<int:pk>', views.PatientDeleteView.as_view(), name="delete"),
    
    path('patients/select_appointment/', views.select_appointment, name="select_appointment"),
    path('patients/delete_appointment/', views.delete_appointment, name="delete_appointment"),
    path('appointment/', views.appointment_list, name="appointment"),
    path('patients/appointment/update/<int:appointment_id>', views.appointment_update, name="appointment_update"),
    
    path('patients/history/update/<int:history_id>', views.history_update, name="history_update"),
    
    path('doctors/list/', views_doc.DoctorListView.as_view(), name="doctor_list"),
    path('doctors/add', views_doc.doctor_create, name="doctor_add"),
    path('doctors/update/<int:doctor_id>', views_doc.doctor_update, name="doctor_update"),
    
    path('patients/history/pdf/<int:patient_id>', views.generatePdf, name="pdf_history"),
    # path('patients/history/pdf/<int:patient_id>', views.GeneratePdf.as_view(), name="pdf_history"),

]


