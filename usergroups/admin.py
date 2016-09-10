from django.contrib import admin
from usergroups.models import UserGroup


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    filter_horizontal = ('representatives',)


admin.site.register(UserGroup, UserGroupAdmin)
