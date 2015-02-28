from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()