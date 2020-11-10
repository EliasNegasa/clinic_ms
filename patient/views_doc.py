from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .forms import DoctorForm
from .models import Doctor
import datetime


class DoctorListView(LoginRequiredMixin, ListView):
    template_name = 'doctor/doc_list.html'
    model = Doctor
    context_object_name = 'doctors'
    paginate_by = 25
    

@login_required()
def doctor_create(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)

        if doctor_form.is_valid():
            firstname = doctor_form.cleaned_data['firstname']
            surname = doctor_form.cleaned_data['surname']
            middlename = doctor_form.cleaned_data['middlename']
            
            phone = doctor_form.cleaned_data['phone']
            specialised = doctor_form.cleaned_data['specialised']


            doctor = Doctor.objects.create(firstname=firstname,
                                             surname=surname,
                                             middlename=middlename,
                                             phone=phone,
                                             specialised=specialised,
                                             created_by=request.user,
                                             updated_by=request.user)

            doctor.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Doctor added successfully!')

            return HttpResponseRedirect(reverse('patient:doctor_list'))
        else:
            return render(request, 'patient/doc_add.html',
                          {"doctor_form": doctor_form})
    return render(request, 'doctor/doc_add.html', {"doctor_form": DoctorForm()})


@login_required()
def doctor_update(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    doctor_form = DoctorForm(request.POST or None, instance=doctor)

    if doctor_form.is_valid():
        doctor.save()

        messages.add_message(request, messages.SUCCESS,
                             'Doctor data updated successfully!')

        return HttpResponseRedirect(reverse('patient:doctor_list'))
    else:
        return render(request, 'doctor/doc_add.html',
                      {"doctor_form": doctor_form})
    return render(request, 'doctor/doc_update.html',
                  {"doctor_form": doctor_form})
