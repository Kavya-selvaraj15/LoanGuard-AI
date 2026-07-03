from django.contrib import admin
from .models import LoanApp, Permission

@admin.register(LoanApp)
class LoanAppAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'risk_level', 'risk_score', 'fraud_probability', 'uploaded_by', 'scanned_at']
    list_filter = ['risk_level', 'is_blacklisted']
    search_fields = ['app_name', 'package_name']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission_name', 'risk_level', 'app']
    list_filter = ['risk_level']
