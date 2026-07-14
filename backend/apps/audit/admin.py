from django.contrib import admin
from apps.audit.models import AuditEvent

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'entity_type', 'record_id', 'ip', 'result')
    list_filter = ('action', 'result', 'timestamp')
    search_fields = ('user__username', 'entity_type', 'record_id', 'ip')
    
    # Make everything read-only in the admin panel
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
