from django.urls import path
from . import views
urlpatterns = [
    path('reports/', views.reports_view, name='reports'),
    path('submit/', views.submit_report_view, name='submit_report'),
]
