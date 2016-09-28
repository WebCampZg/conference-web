from django.contrib import admin
from .models import Conference, Ticket


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'tagline', 'begin_date', 'end_date')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('conference', 'category', 'code', 'promo_code', 'first_name', 'last_name', 'email', 'country', 'purchased_at')
    list_filter = ('conference', 'category', 'promo_code')


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Ticket, TicketAdmin)
