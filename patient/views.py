from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .forms import PatientForm, AddressForm, AppointmentForm
from .models import Patient, Address, Appointment
import datetime


@login_required()
def index(request):
    return render(request, 'patient/index.html', {})


# def patient_list(request):
#     return render(request, 'patient/list.html', {})


class PatientListView(LoginRequiredMixin, ListView):
    template_name = 'patient/list.html'
    model = Patient
    context_object_name = 'patients'


class PatientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'patient/detail.html'
    model = Patient
    context_object_name = 'patient'


@login_required()
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
        context = {
            "search_term": search_term,
            "patients": Patient.objects.filter(
                Q(card_number__icontains=search_term) |
                Q(first__icontains=search_term) |
                Q(last__icontains=search_term) |
                Q(middle__icontains=search_term) |
                # Q(address__icontains=search_term) |
                Q(gender__icontains=search_term) |
                Q(phone__icontains=search_term) |
                Q(created_date__icontains=search_term)
                # Q(appointment__icontains=search_term)
            )
        }
        if not search_term == "":
            return render(request, 'patient/search.html', context)
        else:
            return HttpResponseRedirect(reverse('patient:index'))


@login_required()
def patient_create(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        address_form = AddressForm(request.POST)

        if patient_form.is_valid() and address_form.is_valid():
            first = patient_form.cleaned_data['first']
            sur = patient_form.cleaned_data['sur']
            middle = patient_form.cleaned_data['middle']
            gender = patient_form.cleaned_data['gender']
            age = patient_form.cleaned_data['age']
            phone = patient_form.cleaned_data['phone']
            # appointment = patient_form.cleaned_data['appointment']
            kebele = address_form.cleaned_data['kebele']
            woreda = address_form.cleaned_data['woreda']
            sub_city = address_form.cleaned_data['sub_city']

            address = address_form.save()
            # patient = patient_form.save(False)

            patient = Patient.objects.create(
                first=first,
                last=sur,
                middle=middle,
                gender=gender,
                age=age,
                phone=phone,
                # appointment=appointment,
                address=address,
                created_by=request.user,
                updated_by=request.user)

            # patient.address = address
            patient.save()

            # appointment.strftime('%Y-%m-%d')
            messages.add_message(request, messages.SUCCESS,
                                 'Patient added successfully!')

            return HttpResponseRedirect(reverse('patient:patient_list'))
        else:
            return render(request, 'patient/add.html', {
                "patient_form": patient_form,
                "address_form": address_form
            })
    return render(request, 'patient/add.html', {
        "patient_form": PatientForm(),
        "address_form": AddressForm()
    })


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = 'patient/add.html'
    fields = ['first', 'last', 'middle', 'age',
              'gender', 'phone', 'appointment']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.updated_by = self.request.user
        instance.save()
        messages.success(self.request, 'Patient added successfully!')
        return redirect('patient:patient_list')


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patient/update.html'
    fields = ['first', 'last', 'middle', 'age',
              'gender', 'phone']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        instance.save()
        messages.success(self.request, 'Patient data updated successfully!')
        return redirect('patient:patient_detail', instance.pk)


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patient/delete.html'
    success_url = '../list/'


@login_required()
def appointment_list(request):
    return render(request, 'patient/appointment.html', {
        "appointment": Appointment.objects.all().count(),
        "appointment_today": Appointment.objects.filter(date=datetime.date.today()),
        "appointment_tomorrow": Appointment.objects.filter(date=datetime.date.today() + datetime.timedelta(days=1))
    })


@login_required()
def select_appointment(request):
    data = json.loads(request.body)
    patient_id = data["patientId"]
    appointment_date = data["appointmentDate"]
    action = data["action"]

    Appointment.objects.get_or_create(
        patient=Patient(id=patient_id),
        date=appointment_date
    )
    return JsonResponse(f'Appointment Booked for {Patient.objects.get(pk=patient_id).first} {Patient.objects.get(pk=patient_id).last}', safe=False)


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'patient/delete.html'
    success_url = '../appointment/'