from django import forms

class PathForm(forms.Form):
    path = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',  # Bootstrap class
                'placeholder': 'Enter path',
            }
        )
    )
