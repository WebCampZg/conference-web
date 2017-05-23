from django import forms
from cfp.models import PaperApplication
from django.utils.translation import ugettext as _


class PaperApplicationForm(forms.ModelForm):
    class Meta:
        model = PaperApplication
        exclude = ['cfp', 'applicant', ]

    about_applicant = forms.CharField(
        label=_('About you'),
        help_text='Describe yourself in 140 characters or less. Plain text only. [Public]',
        widget=forms.Textarea(attrs={'rows': 4}))

    biography = forms.CharField(
        label=_('Biography'),
        help_text=('Who are you? Where have you worked? What are your professional interests? '
                   'Up to 10 sentences, use Markdown. [Public]'),
        widget=forms.Textarea(attrs={'rows': 8}))

    speaker_experience = forms.CharField(
        required=False, label=_('Speaker experience'),
        help_text='If you\'ve given talks at other events, please list them.',
        widget=forms.Textarea(attrs={'rows': 8}))

    image = forms.ImageField(
        label=_('Photo'),
        help_text=('Please upload your picture which we may use for our web site and materials. '
                   'Make it square, PNG and at least 400x400px. [Public]'))
