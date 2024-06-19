from django import forms
from django.core.exceptions import ValidationError

from .models import User

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'address'
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error("email", "Данна почта уже зарегистрированна")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли не совпали")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "full_name",
            "birthday",
            "phone",
            "address",
        ]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        
        if phone is None:
            return phone

        if not phone.isascii():
            raise ValidationError("Not allowed simbols!")

        for letter in phone:
            if letter.isalpha():
                raise ValidationError("Not allowed simbols!")

        return phone
