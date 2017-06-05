from django import forms
from cfp.models import PaperApplication, Applicant


class PaperApplicationForm(forms.ModelForm):
    class Meta:
        model = PaperApplication
        exclude = ['cfp', 'applicant', ]

        widgets = {
            "about": forms.Textarea(attrs={'rows': 4})
        }

    about_applicant = forms.CharField(
        label=Applicant._meta.get_field('about').verbose_name,
        help_text=Applicant._meta.get_field('about').help_text,
        widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 140}))

    biography = forms.CharField(
        label=Applicant._meta.get_field('biography').verbose_name,
        help_text=Applicant._meta.get_field('biography').help_text,
        widget=forms.Textarea(attrs={'rows': 8}))

    speaker_experience = forms.CharField(
        required=False,
        label=Applicant._meta.get_field('speaker_experience').verbose_name,
        help_text=Applicant._meta.get_field('speaker_experience').help_text,
        widget=forms.Textarea(attrs={'rows': 8}))

    image = forms.ImageField(
        label=Applicant._meta.get_field('image').verbose_name,
        help_text=Applicant._meta.get_field('image').help_text)


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant

        fields = [
            'about',
            'biography',
            'speaker_experience',
            'image',
        ]

        widgets = {
            'about': forms.Textarea(attrs={'rows': 4, 'maxlength': 140}),
            'biography': forms.Textarea(attrs={'rows': 8}),
            'speaker_experience': forms.Textarea(attrs={'rows': 8}),
        }
