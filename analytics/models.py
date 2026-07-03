from django.db import models


class AnalyticsSummary(models.Model):
    """Aggregated daily analytics snapshot."""
    date = models.DateField(auto_now_add=True, unique=True)
    total_scans = models.IntegerField(default=0)
    dangerous_apps = models.IntegerField(default=0)
    medium_apps = models.IntegerField(default=0)
    safe_apps = models.IntegerField(default=0)
    total_reports = models.IntegerField(default=0)

    def __str__(self):
        return f"Analytics {self.date}"
