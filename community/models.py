from django.db import models
from django.conf import settings


class ScamReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    app_name = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.app_name} by {self.reported_by.username}"

    class Meta:
        ordering = ['-created_at']
