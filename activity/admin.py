from django.contrib import admin

from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    search_fields = ('lesson__title', 'status', 'created_by__username')
    list_filter = ('lesson', 'status', 'created_by')

admin.site.register(Activity, ActivityAdmin)
