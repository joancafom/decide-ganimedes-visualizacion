from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    birthdate = forms.DateTimeField(input_formats=['%d/%m/%Y'], help_text="Formato: dd/mm/YYYY", required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "birthdate", "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.birthdate = self.cleaned_data["birthdate"]

        if commit:
            user.save()
        return user
    