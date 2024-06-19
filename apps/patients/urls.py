from django.urls import path
from .views import (
    HomeView,
    CabinetRedirectView,
    DoctorCabinetView,
    PatientCabinetView,
    PatientResultsListView,
    CreateAssignmentView,
    CreateResultsView,
    UpdateResultsView,
    DeleteResultsView,
    CommitDeleteResultsView
)

app_name = "main"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("cabinet/", CabinetRedirectView.as_view(), name="cabinet"),
    path("cabinet/doctor/", DoctorCabinetView.as_view(), name="doctor_cabinet"),
    path("cabinet/patient/", PatientCabinetView.as_view(), name="patient_cabinet"),
    path("cabinet/assignments/<int:assignment_id>", PatientResultsListView.as_view(), name="assignments_cabinet"),
    path("assignment/create/<int:patient_id>", CreateAssignmentView.as_view(), name="assignment_create"),
    path("mrt/create/<int:assignment_id>", CreateResultsView.as_view(), name="results_create"),
    path("mrt/update/<int:result_id>", UpdateResultsView.as_view(), name="results_update"),
    path("mrt/delete/<int:result_id>", DeleteResultsView.as_view(), name="results_delete"),
    path("mrt/delete/commit/<int:result_id>", CommitDeleteResultsView.as_view(), name="commit_results_delete")
]