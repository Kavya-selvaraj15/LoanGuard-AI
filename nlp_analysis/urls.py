from django.urls import path
from . import views
urlpatterns = [
    path('reviews/', views.review_analysis_view, name='reviews'),
]
