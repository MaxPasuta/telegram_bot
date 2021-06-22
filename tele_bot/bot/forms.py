from django import forms
from .models import Regulations, StatementsOfClaim


class RegulationsForm(forms.ModelForm):

    class Meta:
        model = Regulations
        fields = (
            'question',
            'legal_flag',
            'main_question'
        )
        widgets = {
            'question': forms.Textarea,
        }


class StatementsOfClaimForm(forms.ModelForm):

    class Meta:
        model = StatementsOfClaim
        fields = (
            'title',
            'document',
            'action_algorithm',
            'regulations',

        )
        widgets = {
            'action_algorithm': forms.Textarea,
            'title': forms.Textarea,
        }



