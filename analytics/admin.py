from django.contrib import admin
from .models import AnalyticsSummary

@admin.register(AnalyticsSummary)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_scans', 'dangerous_apps', 'safe_apps']
