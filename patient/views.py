from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .forms import PatientForm, AppointmentForm, HistoryForm
from .models import Patient, Appointment, History, Doctor
import datetime
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf


@login_required()
def index(request):
    return render(request, 'patient/index.html', {})


class PatientListView(LoginRequiredMixin, ListView):
    template_name = 'patient/list.html'
    model = Patient
    context_object_name = 'patients'
    paginate_by = 4


class PatientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'patient/detail.html'
    model = Patient
    context_object_name = 'patient'


@login_required()
def patient_detail(request, patient_id):
    return render(
        request, 'patient/detail.html', {
            'patient': Patient.objects.get(pk=patient_id),
            'histories': History.objects.filter(patient=patient_id),
            'doctors': Doctor.objects.all(),
            'appointments': Appointment.objects.filter(patient=patient_id)
        })


@login_required()
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
        context = {
            "search_term":
            search_term,
            "patients":
            Patient.objects.filter(
                Q(card_number__icontains=search_term)
                | Q(firstname__icontains=search_term)
                | Q(surname__icontains=search_term)
                | Q(middlename__icontains=search_term)
                | Q(gender__icontains=search_term)
                | Q(phone__icontains=search_term)
                | Q(created_date__icontains=search_term)
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

        if patient_form.is_valid():
            firstname = patient_form.cleaned_data['firstname']
            surname = patient_form.cleaned_data['surname']
            middlename = patient_form.cleaned_data['middlename']
            gender = patient_form.cleaned_data['gender']
            age = patient_form.cleaned_data['age']
            phone = patient_form.cleaned_data['phone']

            kebele = patient_form.cleaned_data['kebele']
            woreda = patient_form.cleaned_data['woreda']
            sub_city = patient_form.cleaned_data['sub_city']

            patient = Patient.objects.create(firstname=firstname,
                                             surname=surname,
                                             middlename=middlename,
                                             gender=gender,
                                             age=age,
                                             phone=phone,
                                             kebele=kebele,
                                             woreda=woreda,
                                             sub_city=sub_city,
                                             created_by=request.user,
                                             updated_by=request.user)

            patient.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Patient added successfully!')

            return HttpResponseRedirect(reverse('patient:patient_list'))
        else:
            return render(request, 'patient/add.html',
                          {"patient_form": patient_form})
    return render(request, 'patient/add.html', {"patient_form": PatientForm()})


@login_required()
def patient_update(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient_form = PatientForm(request.POST or None, instance=patient)

    if patient_form.is_valid():
        patient.save()

        messages.add_message(request, messages.SUCCESS,
                             'Patient data updated successfully!')

        return HttpResponseRedirect(reverse('patient:patient_list'))
    else:
        return render(request, 'patient/add.html',
                      {"patient_form": patient_form})
    return render(request, 'patient/update.html',
                  {"patient_form": patient_form})


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patient/update.html'
    fields = ['firstname', 'surname', 'middlename', 'age', 'gender', 'phone']

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
def patient_history(request, patient_id):
    if request.method == 'POST':
        history_form = HistoryForm(request.POST)

        if history_form.is_valid():
            history = history_form.cleaned_data['history']
            doctor = history_form.cleaned_data['doctor']

            history = History.objects.create(
                history=history,
                doctor=Doctor.objects.get(pk=doctor),
                patient=Patient.objects.get(pk=patient_id))

            history.save()

            messages.add_message(request, messages.SUCCESS,
                                 'History added successfully!')

            return HttpResponseRedirect(
                reverse('patient:patient_detail', args=(patient_id, )))
        else:
            return render(request, 'patient/history.html',
                          {"history_form": history_form})

    return render(request, 'patient/history.html',
                  {"history_form": HistoryForm()})


@login_required()
def history_update(request, history_id):
    history = get_object_or_404(History, pk=history_id)
    history_form = HistoryForm(request.POST or None, instance=history)

    if history_form.is_valid():
        history.save()

        messages.add_message(request, messages.SUCCESS,
                             'History updated successfully!')

        return HttpResponseRedirect(
            reverse('patient:patient_detail', args=(history.patient.id, )))
    else:
        return render(request, 'patient/history.html',
                      {"history_form": history_form})
    return render(request, 'patient/history.html',
                  {"history_form": history_form})


@login_required()
def appointment_update(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment_form = AppointmentForm(request.POST or None,
                                       instance=appointment)

    if appointment_form.is_valid():
        appointment.save()

        messages.add_message(request, messages.SUCCESS,
                             'Appointment updated successfully!')

        return HttpResponseRedirect(
            reverse('patient:patient_detail', args=(appointment.patient.id, )))
    else:
        return render(request, 'patient/update_appointment.html',
                      {"appointment_form": appointment_form})
    return render(request, 'patient/update_appointment.html',
                  {"appointment_form": appointment_form})


@login_required()
def appointment_list(request):
    return render(
        request, 'patient/appointment.html', {
            "appointment":
            Appointment.objects.all().count(),
            "appointment_today":
            Appointment.objects.filter(date=datetime.date.today()),
            "appointment_tomorrow":
            Appointment.objects.filter(date=datetime.date.today() +
                                       datetime.timedelta(days=1))
        })


@login_required()
def select_appointment(request):
    data = json.loads(request.body)
    patient_id = data["patientId"]
    appointment_date = data["appointmentDate"]
    assigned_doctor = data["assignedDoctor"]
    action = data["action"]

    Appointment.objects.get_or_create(patient=Patient(id=patient_id),
                                      date=appointment_date,
                                      doctor=Doctor(id=assigned_doctor))
    return JsonResponse(
        f'Appointment Booked for {Patient.objects.get(pk=patient_id).firstname} {Patient.objects.get(pk=patient_id).surname}',
        safe=False)


@login_required()
def delete_appointment(request):
    data = json.loads(request.body)
    print('dfdfdf')
    appointment_id = data["appointmentId"]
    print(appointment_id)
    action = data["action"]

    Appointment.objects.filter(id=appointment_id).delete()
    
    return JsonResponse(
        f'Appointment Deleted',
        safe=False)


# def appointment_delete(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)
#     appointment.delete()
    

def generatePdf(request, patient_id, *args, **kwargs):
    data = {
        'date': datetime.date.today(),
        'patient': Patient.objects.get(pk=patient_id),
        'histories': History.objects.filter(patient=patient_id),
    }
    pdf = render_to_pdf('pdf/pdf_history.html', data)
    return HttpResponse(pdf, content_type='application/pdf')