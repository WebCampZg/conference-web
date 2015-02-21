from django import forms
from cfp.models import AudienceSkillLevel, TShirtSize
from people.models import User


def validate_email_uniqueness(value):
    user_cnt = User.objects.filter(email=value).count()
    if (user_cnt > 0):
        raise forms.ValidationError('Email address already exists')


class PaperApplicationForm(forms.Form):
    title = forms.CharField(help_text='The title of your talk. Keep it short and catchy.', label='Title')
    about = forms.CharField(help_text='Describe your talk in 140 characters or less.', label='What\'s it about')
    abstract = forms.CharField(help_text='You may go in more depth here. Up to 10 sentances, please.', label='Abstract')
    skill_level = forms.ModelChoiceField(queryset=AudienceSkillLevel.objects.all(), label='Audience level',
                                         help_text='Which skill level is this talk most appropriate for?')
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(validators=[validate_email_uniqueness, ])
    about_applicant = forms.CharField(help_text='Describe yourself in 140 characters or less.', label='About you')
    biography = forms.CharField(help_text=('Who are you? Where have you worked? What are your professional interests? '
                                           'This will be used on our web site if you\'re chosen. Up to 10 sentances.'),
                                label='Biography')
    speaker_experience = forms.CharField(required=False, label='Speaker experience',
                                         help_text='If you\'ve given talks at other events, please list them.')
    image = forms.ImageField(help_text=('Please upload your picture which we may use for our web site and materials. '
                                        'Make it square, PNG and at least 400x400px.'))
    tshirt_size = forms.ModelChoiceField(TShirtSize.objects.all(), label='T-shirt size',
                                         help_text='Speakers will receive a fancy speaker WebCamp t-shirt.')
    twitter_handle = forms.CharField(required=False,  label='Twitter',
                                     help_text=('Your twitter handle, if you have one. Enter only your handle, '
                                                'without the @.'))
    github_username = forms.CharField(required=False, label='Github',
                                      help_text=('Your github profile URL, if you have one. Enter only your username, '
                                                 'not the full URL.'))
