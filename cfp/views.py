from django.http.response import Http404
from django.shortcuts import render
from django.views.generic.edit import FormView
from cfp.forms import PaperApplicationForm
from cfp.models import Applicant, PaperApplication, CallForPaper
from people.models import User


class PaperApplicationView(FormView):
    form_class = PaperApplicationForm
    template_name = 'cfp/paper_application.html'

    def dispatch(self, request, *args, **kwargs):
        self.cfp_id = kwargs['cfp_id']
        if not CallForPaper.objects.filter(pk=self.cfp_id).exists():
            raise Http404()
        return super(PaperApplicationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        applicant = self._build_user(form)
        self._build_application(form, applicant)

        return super(PaperApplicationView, self).form_valid(form)

    def _build_user(self, form):
        user = User.objects.create_user(email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

        args = {
            'user': user,
            'about': form.cleaned_data['about_applicant'],
            'biography': form.cleaned_data['biography'],
            'speaker_experience': form.cleaned_data['speaker_experience'],
            'image': form.cleaned_data['image'],
            'tshirt_size': form.cleaned_data['tshirt_size'],
            'twitter_handle': form.cleaned_data['twitter_handle'],
            'github_username': form.cleaned_data['github_username'],
        }
        applicant = Applicant.objects.create(**args)
        return applicant

    def _build_application(self, form, applicant):
        args = {
            'applicant': applicant,
            'title': form.cleaned_data['title'],
            'about': form.cleaned_data['about'],
            'abstract': form.cleaned_data['abstract'],
            'skill_level': form.cleaned_data['skill_level'],
            'cfp_id': self.cfp_id
        }
        application = PaperApplication.objects.create(**args)
        return application
