from django.urls import path
from .api_views import ScamReportListAPIView, ScamReportCreateAPIView

urlpatterns = [
    path('reports/', ScamReportListAPIView.as_view()),
    path('submit/', ScamReportCreateAPIView.as_view()),
]
