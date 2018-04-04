from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from jobs.models import Job


class JobFeed(Feed):
    title = 'WebCampZG Job Board'
    link = reverse_lazy('jobs_list_jobs')

    def item_link(self, item):
        return item.url

    def items(self):
        return Job.objects.order_by('?').all()

    def item_title(self, item):
        return '%s - %s' % (item.sponsor.name, item.title)

    def item_description(self, item):
        return item.text
