from django import forms

from authentication.models import User

MAN = 'M'
WOMEN = 'W'
NON_BINARY = 'N'

DATE_INPUT_FORMATS = ['%d-%m-%Y']


class CensusAddMutipleVotersForm(forms.Form):

    # Preparando valores de los atributos

    SEX_OPTIONS = (
        (MAN, 'Man'),
        (WOMEN, 'Woman'),
        (NON_BINARY, 'Non-binary'),
    )

    # Atributos del formulario

    sex = forms.MultipleChoiceField(label='Sex', choices=SEX_OPTIONS, required=False)
    city = forms.CharField(label='City', required=False)
    age_initial_range = forms.DateField(label='Edad inicial', input_formats=['%d/%m/%Y'], required=False)
    age_final_range = forms.DateField(label='Edad final', required=False)


