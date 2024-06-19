from django.db.models.base import Model as Model
from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import LoginForm, UserCreationForm, UserUpdateForm
from .models import User

class LoginView(View):
    form_class = LoginForm
    template_name = "login.html"

    def get(self, request):
        context = {
            "form": self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if not form.is_valid():
            context = {
                "form": form
            }
            return render(request, self.template_name, context)

        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user is None:
            context = {
                "message": "Пользователь не найден или введён неверный пароль"
            }
            return render(request, self.template_name, context)

        login(request, user)
        return redirect("main:cabinet")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"

    def post(self, request):
        form = self.form_class(data=request.POST)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, self.form_class, context)
        
        user = form.save()
        login(request, user)
        return redirect("main:cabinet")


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "update.html"
    success_url = reverse_lazy("main:index")

    def get_object(self):

        return self.request.user


class LogoutPageView(TemplateView):
    template_name = "logout.html"


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("users:login")
