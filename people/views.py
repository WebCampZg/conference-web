from braces.views._access import LoginRequiredMixin
from django.views.generic.edit import FormView
from people.forms import UserProfileForm


class UserProfileView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm
    template_name = 'people/user_profile.html'

    def get_form(self, form_class):
        return form_class(instance=self.request.user)


