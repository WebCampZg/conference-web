from django import forms
from cfp.models import AudienceSkillLevel, PaperApplication
from django.utils.translation import ugettext as _


class PaperApplicationForm(forms.ModelForm):
    class Meta:
        model = PaperApplication
        exclude = ['cfp', 'applicant', ]

    about_applicant = forms.CharField(help_text='Describe yourself in 140 characters or less.', label=_('About you'),
                                      widget=forms.Textarea(attrs={'rows': 5}))
    biography = forms.CharField(help_text=('Who are you? Where have you worked? What are your professional interests? '
                                           'This will be used on our web site if you\'re chosen. Up to 10 sentences.'),
                                label=_('Biography'), widget=forms.Textarea(attrs={'rows': 5}))
    speaker_experience = forms.CharField(required=False, label=_('Speaker experience'),
                                         help_text='If you\'ve given talks at other events, please list them.',
                                         widget=forms.Textarea(attrs={'rows': 5}))
    image = forms.ImageField(help_text=('Please upload your picture which we may use for our web site and materials. '
                                        'Make it square, PNG and at least 400x400px.'),
                             label=_('Photo'))
