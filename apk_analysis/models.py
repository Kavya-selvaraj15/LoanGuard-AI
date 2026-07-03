from django.db import models
from django.conf import settings


class LoanApp(models.Model):
    RISK_LEVELS = [
        ('safe', 'Safe'),
        ('medium', 'Medium Risk'),
        ('dangerous', 'Dangerous'),
    ]
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loan_apps'
    )
    app_name = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, blank=True)
    developer = models.CharField(max_length=200, blank=True)
    apk_file = models.FileField(upload_to='apks/', blank=True, null=True)
    risk_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='safe')
    fraud_probability = models.FloatField(default=0.0)
    total_permissions = models.IntegerField(default=0)
    dangerous_permissions_count = models.IntegerField(default=0)
    is_blacklisted = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.app_name} - {self.risk_level}"

    class Meta:
        ordering = ['-scanned_at']


class Permission(models.Model):
    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    app = models.ForeignKey(LoanApp, on_delete=models.CASCADE, related_name='permissions')
    permission_name = models.CharField(max_length=200)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='low')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.permission_name} ({self.risk_level})"
