from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('apk/', include('apk_analysis.urls')),
    path('ai/', include('ai_detection.urls')),
    path('nlp/', include('nlp_analysis.urls')),
    path('community/', include('community.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/accounts/', include('accounts.api_urls')),
    path('api/apk/', include('apk_analysis.api_urls')),
    path('api/community/', include('community.api_urls')),
    path('api/analytics/', include('analytics.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
