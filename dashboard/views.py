import datetime
from collections import Counter
from itertools import groupby

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from cfp.models import CallForPaper, PaperApplication, Applicant
from dashboard.models import Comment
from dashboard.forms import CommentForm
from events.models import Event, Ticket
from people.models import TShirtSize
from voting.models import Vote as CommunityVote, VoteToken
from dashboard.models import Vote as CommitteeVote


class ViewAuthMixin(UserPassesTestMixin):
    raise_exception = True

    """Allow access to admins and people on the talk committee"""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated() and (
            user.is_superuser or user.is_talk_committee_member()
        )


class VoteAuthMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated() and user.is_talk_committee_member()


class DashboardView(ViewAuthMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(DashboardView, self).get_context_data(**kwargs)
        ctx['events'] = Event.objects.order_by("-pk")
        return ctx


class EventDetailView(ViewAuthMixin, DetailView):
    model = Event
    template_name = 'dashboard/event.html'


class CallForPapersView(ViewAuthMixin, DetailView):
    model = CallForPaper
    template_name = 'dashboard/call_for_papers.html'

    def get_context_data(self, **kwargs):
        ctx = super(CallForPapersView, self).get_context_data(**kwargs)

        ctx['applications'] = (self.get_object().applications
            .prefetch_related('applicant', 'applicant__user', 'skill_level', 'talk')
            .order_by('pk'))

        return ctx


class ApplicationDetailView(ViewAuthMixin, DetailView):
    model = PaperApplication
    template_name = 'dashboard/application.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        user = self.request.user
        vote = CommitteeVote.objects.filter(user=user, application=self.get_object()).first()
        comments = self.object.comments.order_by("created_at").prefetch_related('author')

        ctx = super(ApplicationDetailView, self).get_context_data(**kwargs)
        ctx.update({
            "comments": comments,
            "allow_voting": user.is_talk_committee_member,
            "score": vote.score if vote else None,
        })
        return ctx


class ApplicantDetailView(ViewAuthMixin, DetailView):
    model = Applicant
    template_name = 'dashboard/applicant.html'

    def get_context_data(self, **kwargs):
        applicant = self.get_object()
        applications = applicant.applications.order_by("-created_at")

        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "applications": applications,
        })
        return ctx


class ApplicationRateView(VoteAuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))
        score = int(request.POST.get('score'))

        if score < 1 or score > 5:
            raise ValidationError("Invalid score")

        application = get_object_or_404(PaperApplication, pk=application_id)

        obj, created = CommitteeVote.objects.update_or_create(
            user=request.user, application=application, defaults={"score": score})

        return HttpResponse(status=201 if created else 200)


class ApplicationUnrateView(VoteAuthMixin, View):

    def post(self, request, *args, **kwargs):
        application_id = int(request.POST.get('application_id'))

        application = get_object_or_404(PaperApplication, pk=application_id)

        CommitteeVote.objects.filter(user=request.user, application=application).delete()

        return HttpResponse(status=204)


class CommunityVoteView(ViewAuthMixin, TemplateView):
    template_name = 'dashboard/community-vote.html'

    def get_context_data(self, **kwargs):
        ctx = super(CommunityVoteView, self).get_context_data(**kwargs)

        ctx['vote_count'] = CommunityVote.objects.count()
        ctx['participants_voted'] = CommunityVote.objects.values('user').distinct().count()
        ctx['participants_total'] = VoteToken.objects.count()

        applications = (PaperApplication.objects
            .filter(exclude=False)
            .prefetch_related('votes', 'applicant', 'applicant__user', 'skill_level'))

        ctx['applications'] = sorted(applications, key=lambda x: x.votes_count, reverse=True)

        return ctx


class EventTicketsView(ViewAuthMixin, ListView):
    model = Ticket
    template_name = 'dashboard/event-tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        qs = super(EventTicketsView, self).get_queryset()
        event_id = self.kwargs.get('pk')
        self.event = get_object_or_404(Event, pk=event_id)
        return qs.filter(event=self.event)

    def get_context_data(self, **kwargs):
        ctx = super(EventTicketsView, self).get_context_data(**kwargs)

        tickets = self.object_list.prefetch_related('tshirt_size')

        if tickets:
            ctx['countries'] = self.most_common(tickets, lambda t: t.country)
            ctx['categories'] = self.most_common(tickets, lambda t: t.category)
            ctx['tshirts'] = self.tshirt_sizes(tickets)
            ctx['tickets_by_date'] = self.tickets_by_date(tickets)

        ctx['event'] = self.event
        ctx['tickets'] = tickets

        return ctx

    def date_range(self, start, end):
        dates = []
        date = start
        while date <= end:
            dates.append(date)
            date += datetime.timedelta(days=1)
        return dates

    def tickets_by_date(self, tickets):
        groups = groupby(tickets, lambda t: t.purchased_at.date())
        tickets_by_date = {k: len(list(v)) for k, v in groups}

        # Create a list of all dates from the first ticket bought until today
        start_date = min(tickets_by_date.keys())
        today = datetime.date.today()
        dates = self.date_range(start_date, today)

        return [(date, tickets_by_date.get(date, 0)) for date in dates]

    def tshirt_sizes(self, tickets):
        sizes = [t.tshirt_size_id for t in tickets]
        most_common = Counter(sizes).most_common()
        most_common_dict = dict(most_common)
        top_count = most_common[0][1]

        return [{
            "value": size.name,
            "count": most_common_dict.get(size.id, 0),
            "width": most_common_dict.get(size.id, 0) * 100 / top_count,
        } for size in TShirtSize.objects.all()]

    def most_common(self, tickets, value_fn):
        values = [value_fn(t) for t in tickets]
        most_common = Counter(values).most_common()

        return [{
            "value": x[0],
            "count": x[1],
            "width": (float(100 * x[1]) / most_common[0][1]), # for drawing progress bars
        } for x in most_common]


class BaseCommentEditView(ViewAuthMixin, ModelFormMixin, ProcessFormView):
    model = Comment
    form_class = CommentForm
    template_name = 'dashboard/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.application = PaperApplication.objects.get(pk=self.kwargs.get('application_pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "application": self.application
        })
        return ctx

    def get_success_url(self):
        return reverse("dashboard:application_detail", kwargs={"pk": self.application.pk})


class CommentCreateView(BaseCommentEditView, CreateView):
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.application = self.application
        comment.author = self.request.user
        comment.save()

        return HttpResponseRedirect(self.get_success_url())


class CommentUpdateView(BaseCommentEditView, UpdateView):
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class CommentDeleteView(BaseCommentEditView, DeleteView):
    template_name = 'dashboard/comment_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
