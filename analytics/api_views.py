from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apk_analysis.models import LoanApp
from community.models import ScamReport

class AnalyticsSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        apps = LoanApp.objects.all()
        return Response({
            'total': apps.count(),
            'safe': apps.filter(risk_level='safe').count(),
            'medium': apps.filter(risk_level='medium').count(),
            'dangerous': apps.filter(risk_level='dangerous').count(),
            'reports': ScamReport.objects.count(),
        })
