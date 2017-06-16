from django.views.generic import ListView, DetailView
from config.utils import get_active_event
from workshops.models import Workshop


class WorkshopListView(ListView):
    template_name = 'workshops/list_workshops.html'
    model = Workshop
    context_object_name = 'workshops'

    def get_queryset(self):
        event = get_active_event()

        return (super().get_queryset()
                       .filter(event=event)
                       .prefetch_related('applicant', 'applicant__user', 'skill_level')
                       .order_by('title'))


class WorkshopDetailView(DetailView):
    template_name = 'workshops/view_workshop.html'
    model = Workshop
