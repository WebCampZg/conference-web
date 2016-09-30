from django.contrib import admin
from .models import Conference, Ticket
from django.core.urlresolvers import reverse

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'tagline', 'begin_date', 'end_date')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('conference', 'category', 'code', '_user', 'country', 'purchased_at')
    list_filter = ('conference', 'category', 'promo_code')

    def _user(self, ticket):
        label = ticket.first_name + " " + ticket.last_name
        if ticket.user:
            link = reverse("admin:people_user_change", args=(ticket.user.id,))
            return '<a href="%s">%s</a>' % (link, label)
        else:
            return label

    _user.allow_tags = True


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Ticket, TicketAdmin)
