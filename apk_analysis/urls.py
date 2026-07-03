from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_view, name='upload'),
    path('result/<int:pk>/', views.scan_result_view, name='scan_result'),
    path('history/', views.history_view, name='history'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
