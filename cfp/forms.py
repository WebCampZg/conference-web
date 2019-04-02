from django import forms
from cfp.models import PaperApplication, Applicant


class PaperApplicationForm(forms.ModelForm):
    class Meta:
        model = PaperApplication
        fields = (
            'type',
            'title',
            'about',
            'abstract',
            'skill_level',
            'accomodation_required',
            'travel_expenses_required',
            'extra_info',
            'grant_email_contact',
            'grant_process_data',
            'grant_publish_data',
            'grant_publish_video',
        )

        help_texts = {
            'type':
                'What are you applying for? Note that there are fewer slots for long talks and '
                'workshops and applying for a shorter one gives you better chances of being '
                'accepted.',
        }

        widgets = {
            "about": forms.Textarea(attrs={'rows': 4})
        }

    title = forms.CharField(
        max_length=50, required=True,
        help_text=PaperApplication._meta.get_field('title').help_text)

    grant_email_contact = forms.BooleanField(
        required=True,
        label='Yes, I wish to be contacted by email regarding my talk submission',
        help_text='We will let you know whether your talk was selected, and if selected, '
                  'coordinate your appearance at the conference.')

    grant_process_data = forms.BooleanField(
        required=True,
        label='I agree that all data in this form may be used for the purposes of talk selection',
        help_text='The talks selection committee will have access to this data and use it to '
                  'rate your submission.')

    grant_publish_data = forms.BooleanField(
        required=True,
        label='I agree that, if my talk is selected, data marked [Public] may be published publicly',
        help_text='This includes publishing on our web site and social media platforms including '
                  'Facebook and Twitter.')

    grant_publish_video = forms.BooleanField(
        required=True,
        label='I agree that my talk may be recorded and published publicly',
        help_text='This includes uploading the video to youtube.com, archive.org and embedding '
                  'on our web site.')

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
