from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['app', 'sentiment', 'polarity', 'is_scam_review', 'created_at']
    list_filter = ['sentiment', 'is_scam_review']
