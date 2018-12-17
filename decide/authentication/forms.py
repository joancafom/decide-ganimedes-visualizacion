from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    SEX_OPTIONS = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('N', 'Non-binary'),
    )
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    birthdate = forms.DateTimeField(input_formats=['%d/%m/%Y'], help_text="Formato: dd/mm/YYYY", required=False)
    city = forms.CharField(required=True)
    sex = forms.ChoiceField(choices=SEX_OPTIONS, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "birthdate", "city", "sex", "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.city = self.cleaned_data["city"]
        user.sex = self.cleaned_data["sex"]

        if commit:
            user.save()
        return user
    