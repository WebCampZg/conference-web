from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from labels.models import Label
from dashboard.views import ViewAuthMixin
from labels.forms import LabelForm


class LabelListView(ViewAuthMixin, ListView):
    model = Label
    template_name = 'dashboard/label_list.html'


class LabelCreateView(ViewAuthMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'dashboard/label_form.html'
    success_url = reverse_lazy('dashboard:label-list')


class LabelDeleteView(ViewAuthMixin, DeleteView):
    model = Label
    template_name = 'dashboard/label_delete.html'
    success_url = reverse_lazy('dashboard:label-list')
