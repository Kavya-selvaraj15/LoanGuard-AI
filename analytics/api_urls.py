from django.urls import path
from .api_views import AnalyticsSummaryAPIView
urlpatterns = [
    path('summary/', AnalyticsSummaryAPIView.as_view(), name='api-analytics'),
]
