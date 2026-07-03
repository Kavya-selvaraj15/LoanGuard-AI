from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LoanApp, Permission
from .utils import (
    extract_permissions_from_apk,
    calculate_permission_risk_score,
    simulate_apk_scan,
)
from ai_detection.predictor import predict_fraud
import os, tempfile


class APKUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        app_name = request.data.get('app_name', 'Unknown App')

        if 'apk_file' in request.FILES:
            apk_file = request.FILES['apk_file']
            with tempfile.NamedTemporaryFile(delete=False, suffix='.apk') as tmp:
                for chunk in apk_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            permissions, package, _ = extract_permissions_from_apk(tmp_path)
            os.unlink(tmp_path)
        else:
            permissions, package, _ = simulate_apk_scan(app_name)

        perm_score = calculate_permission_risk_score(permissions)
        fraud_result = predict_fraud(permissions)
        fraud_prob = fraud_result['fraud_probability']
        risk_level = fraud_result['risk_level']
        final_score = round((perm_score * 0.6 + fraud_prob * 0.4), 2)

        loan_app = LoanApp.objects.create(
            uploaded_by=request.user,
            app_name=app_name,
            package_name=package,
            risk_score=final_score,
            risk_level=risk_level.lower().replace(' ', '_').replace('medium_risk', 'medium'),
            fraud_probability=fraud_prob,
            total_permissions=len(permissions),
            dangerous_permissions_count=sum(1 for p in permissions if p['risk_level'] == 'high'),
        )
        for p in permissions:
            Permission.objects.create(
                app=loan_app,
                permission_name=p['name'],
                risk_level=p['risk_level'],
                description=p['description'],
            )

        return Response({
            'app_id': loan_app.id,
            'app_name': app_name,
            'risk_level': risk_level,
            'fraud_probability': fraud_prob,
            'risk_score': final_score,
            'permissions': permissions,
        })


class ScanResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            app = LoanApp.objects.get(pk=pk, uploaded_by=request.user)
        except LoanApp.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        perms = list(app.permissions.values('permission_name', 'risk_level', 'description'))
        return Response({
            'id': app.id,
            'app_name': app.app_name,
            'risk_level': app.risk_level,
            'fraud_probability': app.fraud_probability,
            'risk_score': app.risk_score,
            'permissions': perms,
            'scanned_at': app.scanned_at,
        })


class ScanHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = LoanApp.objects.filter(uploaded_by=request.user).values(
            'id', 'app_name', 'risk_level', 'risk_score', 'fraud_probability', 'scanned_at'
        )
        return Response(list(apps))
