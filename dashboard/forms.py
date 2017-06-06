from django import forms

from dashboard.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = [
            'text',
            'link',
        ]

        help_texts = {
            "text": "Use Markdown for formatting comments, but avoid headers."
        }

    def clean(self):
        cleaned_data = super().clean()

        text = cleaned_data.get("text")
        link = cleaned_data.get("link")

        if not text and not link:
            raise forms.ValidationError("Either text or a link must be populated.")

        return cleaned_data
