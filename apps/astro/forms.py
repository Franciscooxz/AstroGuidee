from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electronico")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Tu nombre de usuario",
            "email": "tucorreo@ejemplo.com",
            "password1": "Crea una contrasena",
            "password2": "Repite la contrasena",
        }
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "field"
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "field", "placeholder": "Tu usuario"})
        self.fields["password"].widget.attrs.update(
            {"class": "field", "placeholder": "Tu contrasena"}
        )


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "field"
