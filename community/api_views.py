from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ScamReport

class ScamReportListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        reports = ScamReport.objects.values(
            'id','app_name','description','status','upvotes','created_at'
        )
        return Response(list(reports))

class ScamReportCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        report = ScamReport.objects.create(
            reported_by=request.user,
            app_name=data.get('app_name',''),
            package_name=data.get('package_name',''),
            description=data.get('description',''),
        )
        return Response({'id': report.id, 'message': 'Report submitted.'}, status=201)
