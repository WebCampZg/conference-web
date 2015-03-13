from django import forms
from django.utils.translation import ugettext as _
from people.models import TShirtSize


class SignupForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('First name')}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Last name')}))
    github = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Github username')}))
    twitter = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Twitter handle')}))
    tshirt_size = forms.ModelChoiceField(queryset=TShirtSize.objects.all(), empty_label=None,
                                         widget=forms.Select(attrs={'placeholder': _('T-shirt size')}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.github = self.cleaned_data['github']
        user.twitter = self.cleaned_data['twitter']
        user.tshirt_size = self.cleaned_data['tshirt_size']
        user.save()
