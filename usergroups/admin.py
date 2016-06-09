from django.contrib import admin
from usergroups.models import UserGroup

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


admin.site.register(UserGroup, UserGroupAdmin)