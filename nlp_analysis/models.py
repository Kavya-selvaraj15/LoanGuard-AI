from django.db import models
from apk_analysis.models import LoanApp


class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]
    app = models.ForeignKey(LoanApp, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    polarity = models.FloatField(default=0.0)
    is_scam_review = models.BooleanField(default=False)
    scam_keywords_found = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.app.app_name} [{self.sentiment}]"
