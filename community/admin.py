from django.contrib import admin
from .models import ScamReport

@admin.register(ScamReport)
class ScamReportAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'reported_by', 'status', 'upvotes', 'created_at']
    list_filter = ['status']
    actions = ['verify_reports', 'reject_reports']

    def verify_reports(self, request, queryset):
        queryset.update(status='verified')
    verify_reports.short_description = 'Mark selected as verified'

    def reject_reports(self, request, queryset):
        queryset.update(status='rejected')
    reject_reports.short_description = 'Mark selected as rejected'
