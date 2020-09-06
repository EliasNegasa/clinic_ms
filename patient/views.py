from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient


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
                Q(address__icontains=search_term) |
                Q(gender__icontains=search_term) |
                Q(phone__icontains=search_term) |
                Q(created_date__icontains=search_term) |
                Q(appointment__icontains=search_term)
            )
        }
        if not search_term == "":
            return render(request, 'patient/search.html', context)
        else:
            return HttpResponseRedirect(reverse('patient:index'))


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = 'patient/add.html'
    fields = ['first', 'last', 'middle', 'age', 'gender', 'phone', 'address', 'appointment']

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
    fields = ['first', 'last', 'middle', 'age', 'gender', 'phone', 'address', 'appointment']

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
