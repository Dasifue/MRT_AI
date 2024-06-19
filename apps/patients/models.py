from django.db import models


class DoctorPatientAssignment(models.Model):
    doctor = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name='assigned_patients')
    patient = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name='assigned_doctors')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient')
        verbose_name = 'Назначение врача'
        verbose_name_plural = 'Назначения врачей'

    def __str__(self):
        return f'Врач {self.doctor.full_name} лечит пациента {self.patient.full_name}'


class Results(models.Model):
    assignment = models.ForeignKey(
        DoctorPatientAssignment, verbose_name="Назначение", on_delete=models.CASCADE, related_name='results')
    mrt_picture = models.ImageField("МРТ Рисунок", upload_to="images")
    diagnosis = models.CharField(
        "Диагноз", max_length=50, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Результат исследования"
        verbose_name_plural = "Результаты исследований"
