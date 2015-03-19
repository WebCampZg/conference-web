from braces.views._access import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model

from people.forms import UserProfileForm
from cfp.models import Applicant, PaperApplication


UserModel = get_user_model()


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UserProfileForm
    template_name = 'people/user_profile.html'

    def get_context_data(self, **kwargs):
        c = super(UserProfileView, self).get_context_data(**kwargs)
        try:
            c['applications'] = self.request.user.applicant.applications.all()
        except Applicant.DoesNotExist, PaperApplication.DoesNotExist:
            c['applications'] = []
        return c

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('user_profile')

