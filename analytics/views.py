from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apk_analysis.models import LoanApp
from community.models import ScamReport

@login_required
def analytics_view(request):
    apps = LoanApp.objects.all()
    context = {
        'total': apps.count(),
        'safe': apps.filter(risk_level='safe').count(),
        'medium': apps.filter(risk_level='medium').count(),
        'dangerous': apps.filter(risk_level='dangerous').count(),
        'reports': ScamReport.objects.count(),
    }
    return render(request, 'analytics/analytics.html', context)
