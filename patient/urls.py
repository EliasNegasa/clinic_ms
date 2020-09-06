from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path('', views.index, name="index"),
    # path('list', views.patient_list, name="list"),
    path('list/', views.PatientListView.as_view(), name="patient_list"),
    path('detail/<int:pk>', views.PatientDetailView.as_view(), name="patient_detail"),
    path('search', views.search, name="search"),
    path('patients/add', views.PatientCreateView.as_view(), name="add"),
    path('patients/update/<int:pk>', views.PatientUpdateView.as_view(), name="update"),
    path('patients/delete/<int:pk>', views.PatientDeleteView.as_view(), name="delete"),
]


