from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

from apps.patients.models import DoctorPatientAssignment

class UserManager(BaseUserManager):

    def create(self, **kwargs):
        password = kwargs.get("password")
        if password is not None:
            kwargs['password'] = make_password(password)
        return super().create(**kwargs)

    def create_user(self, email, password, **kwargs):
        if not email:
            raise AttributeError("User email not specified")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):

        kwargs.update(
            {
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "position": "ADMIN",
            }
        )
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    POSITION_CHOICES = (
        ('ADMIN', 'Администратор'),
        ('DOCTOR', 'Врач'),
        ('PATIENT', 'Пациент'),
    )
    full_name = models.CharField("ФИО", max_length=50)
    birthday = models.DateField("Дата рождения", null=True, blank=True)
    email = models.EmailField(verbose_name="Почта", unique=True)
    position = models.CharField("Позиция пользователя", max_length=20, choices=POSITION_CHOICES, default="PATIENT")
    phone = models.CharField("Контакты", max_length=50, null=True, blank=True)
    address = models.CharField("Место проживания", max_length=256, null=True, blank=True)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        positions = dict(self.POSITION_CHOICES)

        if self.full_name is None:
            return f"{positions[self.position]} №{self.id}"
        return f"{positions[self.position]} №{self.id} - {self.full_name}"


    def assign_patient(self, patient):
        if self.position == 'PATIENT':
            raise ValueError('Назначение пациентов возможно только для врачей.')
        if patient.position != 'PATIENT':
            raise ValueError('Можно назначать только пациентов.')
        assignment, created = DoctorPatientAssignment.objects.get_or_create(doctor=self, patient=patient)
        return assignment

    def is_assigned_to(self, patient):
        return DoctorPatientAssignment.objects.filter(doctor=self, patient=patient).exists()

    def get_assigned_patients(self):
        if self.position != 'DOCTOR':
            return []
        return self.assigned_patients.all()

