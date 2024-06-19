from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.models import User
from apps.users.mixins import IsDoctorMixin, IsPatientMixins

from .models import DoctorPatientAssignment, Results
from .forms import MRTResultForm, UpdateMRTResultForm

from .tasks import predict_tumor

class HomeView(TemplateView):

    template_name = "index.html"

class CabinetRedirectView(LoginRequiredMixin, View):

    def get(self, request):
        position = request.user.position

        if position == "DOCTOR":
            return redirect("main:doctor_cabinet")
        elif position == "PATIENT":
            return redirect("main:patient_cabinet")
        elif position == "ADMIN":
            return render(request, "cabinet.html")
        else:
            return render(request, "error.html", {"error": "Ошибка"})


class DoctorCabinetView(LoginRequiredMixin, IsDoctorMixin, ListView):
    queryset = User.objects.filter(position="PATIENT")
    template_name = "doctor_cabinet.html"

    def get_context_data(self, **kwargs):
        assignments = self.request.user.assigned_patients.all()

        assigned_patients_id = [assignment['patient_id'] for assignment in assignments.values()]
        free_patients = User.objects.filter(position="PATIENT").exclude(id__in=assigned_patients_id)

        context = {
            "free_patients": free_patients,
            "assignments": assignments, 
        }
        return context


class PatientCabinetView(LoginRequiredMixin, IsPatientMixins, ListView):
    template_name = "patient_cabinet.html"
    context_object_name = "assignments"

    def get_queryset(self):
        return self.request.user.assigned_doctors.all()


class CreateAssignmentView(LoginRequiredMixin, IsDoctorMixin, View):

    def get(self, request, patient_id):
        patient = get_object_or_404(User, id=patient_id)
        try:
            self.request.user.assign_patient(patient)
        except ValueError as error:
            return render(request, "error.html", {"error": error})
        return redirect(request.META.get('HTTP_REFERER', '/'))


class PatientResultsListView(LoginRequiredMixin, View):

    def get(self, request, assignment_id):
        assignment = get_object_or_404(DoctorPatientAssignment, id=assignment_id)
        if self.request.user not in (assignment.doctor, assignment.patient) and request.user.position != "ADMIN":
            return render(request, "error.html", {"error": "У вас нет доступа для этой страницы"})

        context = {
            "assignment": assignment
        }
        return render(request, "results.html", context)


class CreateResultsView(LoginRequiredMixin, IsDoctorMixin, View):
    template_name = "create_results.html"

    def get(self, request, assignment_id):
        assignment = get_object_or_404(DoctorPatientAssignment, id=assignment_id)
        if self.request.user not in (assignment.doctor, assignment.patient) and request.user.position != "ADMIN":
            return render(request, "error.html", {"error": "У вас нет доступа для этой страницы"})


        form = MRTResultForm()
        context = {
            "form": form,
            "assignment": assignment,
        }
        return render(request, self.template_name, context)

    def post(self, request, assignment_id):
        form = MRTResultForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            results = form.save(commit=False)
            results.assignment_id = assignment_id
            results.save()
            predict_tumor.delay(results.id)
            return redirect("main:assignments_cabinet", assignment_id=assignment_id)

        context = {
            "form": form,
        }
        return render(request, self.template_name, context)
    
class UpdateResultsView(LoginRequiredMixin, IsDoctorMixin, View):
    template_name = "update_results.html"
    form_class = UpdateMRTResultForm

    def get(self, request, result_id):
        result = get_object_or_404(Results, id=result_id)

        if self.request.user not in (result.assignment.doctor, result.assignment.patient) and request.user.position != "ADMIN":
            return render(request, "error.html", {"error": "У вас нет доступа для этой страницы"})
        form = self.form_class(instance=result)
        context = {
            "result": result,
            "form": form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, result_id):
        result = get_object_or_404(Results, id=result_id)
        form = self.form_class(data=request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect("main:assignments_cabinet", assignment_id=result.assignment.id)

        context = {
            "form": form,
            "result": result,
        }
        return render(request, self.template_name, context)


class DeleteResultsView(LoginRequiredMixin, IsDoctorMixin, View):

    def get(self, request, result_id):
        result = get_object_or_404(Results, id=result_id)
        context = {
            "result": result
        }
        return render(request, "delete_results.html", context)


class CommitDeleteResultsView(LoginRequiredMixin, IsDoctorMixin, View):

    def get(self, request, result_id):
        result = get_object_or_404(Results, id=result_id)
        assignment_id = result.assignment.id

        result.delete()
        return redirect("main:assignments_cabinet", assignment_id=assignment_id)
