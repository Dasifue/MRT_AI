from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import UserCreationForm
from apps.patients.models import DoctorPatientAssignment


admin.site.unregister(Group)

class AssignmentsInline(admin.StackedInline):
    model = DoctorPatientAssignment
    fk_name = "doctor"
    extra = 0

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ("id", "email", "full_name", "phone")
    list_display_links = ("id", "email", "full_name")
    list_filter = ("position",)
    search_fields = ("full_name", "phone", "address", "email")
    ordering = ["position"]
    inlines = [AssignmentsInline]
    fieldsets = [
        (
            "Данные пользователя",
            {
                "fields": [
                    "position",
                    "full_name",
                    "email",
                    "phone",
                    "birthday",
                    "address",
                ]
            }
        ),
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2')}
        ),
    ]