from django import forms
from rest_framework.exceptions import ValidationError

from authentication.models import User
from voting.models import Voting
from django.db.models import Q

# Contiene todos los formularios de la aplicación Census

# Constantes

MAN = 'M'
WOMEN = 'W'
NON_BINARY = 'N'

DATE_INPUT_FORMATS = ['%d/%m/%Y']

class CensusAddMutipleVotersForm(forms.Form):
    # Preparando valores de los atributos

    SEX_OPTIONS = (
        (MAN, 'Man'),
        (WOMEN, 'Woman'),
        (NON_BINARY, 'Non-binary'),
    )

    voting = forms.ModelChoiceField(label='Seleccione una votación', empty_label="-",
                                    queryset=Voting.objects.all().filter(start_date__isnull=False,
                                                                         end_date__isnull=True), required=True,)

    # Atributos del formulario

    sex = forms.MultipleChoiceField(label='Sex', choices=SEX_OPTIONS, required=False)

    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'placeholder': 'Ej: Sevilla'}), required=False)

    # TODO: Implementar city para el nombre que aparezca en la selección multiple sea city y no lo que aparece en el
    #       método __str___
    # city = forms.ModelMultipleChoiceField(label='City', initial='City',
    #           queryset=User.objects.all().distinct().order_by('city'))

    age_initial_range = forms.DateField(label='Edad de inicio:',
                                        widget=forms.TextInput(attrs={'placeholder': 'Ej: 22/12/1990'}),
                                        input_formats=DATE_INPUT_FORMATS, required=False)

    age_final_range = forms.DateField(label='Edad final',
                                      widget=forms.TextInput(attrs={'placeholder': 'Ej: 21/10/2008'}),
                                      required=False)
