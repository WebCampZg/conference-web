from django import forms
from django.forms.widgets import TextInput

from labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name', 'bg_color')
        widgets = {
            "bg_color": TextInput(attrs={"type": "color"}),
        }
        labels = {
            "bg_color": "Color",
        }
