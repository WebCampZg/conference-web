from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http.response import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView

from braces.views._access import LoginRequiredMixin
from cfp.forms import PaperApplicationForm, ApplicantForm
from cfp.models import Applicant, PaperApplication
from config.utils import get_active_cfp


class PaperApplicationBaseView(SuccessMessageMixin, LoginRequiredMixin):
    model = PaperApplication
    form_class = PaperApplicationForm
    template_name = 'cfp/cfp_form.html'
    success_message = "You have successfully submitted your application."

    def get_context_data(self, **kwargs):
        c = super(PaperApplicationBaseView, self).get_context_data(**kwargs)
        c.update({
            'cfp': self.cfp
        })
        return c

    def form_valid(self, form):
        applicant = self._build_or_update_applicant(form)
        form.instance.applicant_id = applicant.pk
        form.instance.cfp_id = self.cfp.pk

        return super(PaperApplicationBaseView, self).form_valid(form)

    def get_initial(self):
        initial = super(PaperApplicationBaseView, self).get_initial()
        try:
            applicant = self.request.user.applicant
            initial.update({
                'about_applicant': applicant.about,
                'biography': applicant.biography,
                'company_name': applicant.company_name,
                'speaker_experience': applicant.speaker_experience,
                'image': applicant.image,
            })
        except Applicant.DoesNotExist:
            pass

        return initial

    def _build_or_update_applicant(self, form):
        user = self.request.user
        args = {
            'user': user,
            'about': form.cleaned_data['about_applicant'],
            'biography': form.cleaned_data['biography'],
            'company_name': form.cleaned_data['company_name'],
            'speaker_experience': form.cleaned_data['speaker_experience'],
            'image': form.cleaned_data['image'],
        }

        applicant, created = Applicant.objects.update_or_create(user=user, defaults=args)
        return applicant

    def get_success_url(self):
        return reverse('user_profile')


class PaperApplicationCreateView(PaperApplicationBaseView, CreateView):

    def dispatch(self, request, *args, **kwargs):
        self.cfp = get_active_cfp()

        if not self.cfp:
            return HttpResponseForbidden("Call for proposals is not active.")

        return super().dispatch(request, *args, **kwargs)


class PaperApplicationUpdateView(PaperApplicationBaseView, UpdateView):
    success_message = "You have successfully updated your application."

    def dispatch(self, request, *args, **kwargs):
        self._check_allowed(request.user)
        self.cfp = self.get_object().cfp

        return super().dispatch(request, *args, **kwargs)

    def _check_allowed(self, user):
        allow = False
        application = self.get_object()
        try:
            if application.applicant_id == user.applicant.pk:
                allow = True
        except Applicant.DoesNotExist:
            pass

        if not allow:
            raise Http404()


def cfp_announcement(request):
    return render(request, 'cfp/cfp_announcement.html')


class ApplicantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ApplicantForm
    template_name = "cfp/applicant_form.html"

    def get_object(self):
        try:
            return self.request.user.applicant
        except Applicant.DoesNotExist:
            return Applicant(user=self.request.user)

    def get_success_url(self):
        return reverse('user_profile')
