from django import forms
from people.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'github', 'twitter', 'tshirt_size',]