from django.contrib import admin

# Register your models here.
from logs import  models

class EventLogAdmin(admin.ModelAdmin):
    list_display = ('name','colored_event_type','asset','component','detail','date','user')
    search_fields = ('asset',)
    list_filter = ('event_type','component','date','user')
admin.site.register(models.EventLog,EventLogAdmin)
admin.site.register(models.UserLoginLog)
admin.site.register(models.OperationLog)