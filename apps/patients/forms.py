from django import forms

from .models import Results


class MRTResultForm(forms.ModelForm):

    class Meta:
        model = Results
        fields = [
            "mrt_picture",
            "diagnosis",
            "description"
        ]

class UpdateMRTResultForm(forms.ModelForm):

    class Meta:
        model = Results
        fields = [
            "diagnosis",
            "description",
        ]
