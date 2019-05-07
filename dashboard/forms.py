from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from cfp.models import PaperApplication
from dashboard.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = [
            'text',
            'link',
            'is_private',
        ]

        help_texts = {
            "text": "Use Markdown for formatting comments, but avoid headers.",
            "link": "Links to youtube videos will automatically be expanded.",
            "is_private": "Private comments are visible only to you.",
        }

    def clean(self):
        cleaned_data = super().clean()

        text = cleaned_data.get("text")
        link = cleaned_data.get("link")

        if not text and not link:
            raise forms.ValidationError("Either text or a link must be populated.")

        return cleaned_data


class ApplicationFilterForm(forms.Form):
    types = forms.MultipleChoiceField(
        choices=PaperApplication.TYPES,
        widget=CheckboxSelectMultiple(),
        required=False,
        label="",
    )
