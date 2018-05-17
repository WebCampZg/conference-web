from django import forms
from cfp.models import PaperApplication, Applicant


class PaperApplicationForm(forms.ModelForm):
    class Meta:
        model = PaperApplication
        fields = (
            'title',
            'about',
            'abstract',
            'skill_level',
            'duration',
            'accomodation_required',
            'travel_expenses_required',
            'extra_info',
        )

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

    company_name = forms.CharField(
        required=False,
        label=Applicant._meta.get_field('company_name').verbose_name,
        help_text=Applicant._meta.get_field('company_name').help_text)

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
            'company_name',
            'speaker_experience',
            'image',
        ]

        widgets = {
            'about': forms.Textarea(attrs={'rows': 4, 'maxlength': 140}),
            'biography': forms.Textarea(attrs={'rows': 8}),
            'speaker_experience': forms.Textarea(attrs={'rows': 8}),
        }
