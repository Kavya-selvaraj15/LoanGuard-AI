from django.urls import path
from .api_views import APKUploadAPIView, ScanResultAPIView, ScanHistoryAPIView

urlpatterns = [
    path('upload/', APKUploadAPIView.as_view(), name='api-apk-upload'),
    path('result/<int:pk>/', ScanResultAPIView.as_view(), name='api-scan-result'),
    path('history/', ScanHistoryAPIView.as_view(), name='api-history'),
]
