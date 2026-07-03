from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LoanApp, Permission
from .utils import (
    extract_permissions_from_apk,
    calculate_permission_risk_score,
    simulate_apk_scan,
)
from ai_detection.predictor import predict_fraud
from nlp_analysis.analyzer import analyze_reviews_bulk
import os


@login_required
def upload_view(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name', 'Unknown App')
        reviews_text = request.POST.get('reviews', '')
        use_demo = request.POST.get('use_demo', False)

        # Determine permissions source
        if 'apk_file' in request.FILES and request.FILES['apk_file']:
            apk_file = request.FILES['apk_file']
            # save temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.apk') as tmp:
                for chunk in apk_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            permissions, package, detected_name = extract_permissions_from_apk(tmp_path)
            os.unlink(tmp_path)
            if detected_name and detected_name != os.path.basename(tmp_path):
                app_name = detected_name
        else:
            # Demo simulation mode
            permissions, package, _ = simulate_apk_scan(app_name)

        # Calculate risk score
        perm_score = calculate_permission_risk_score(permissions)

        # AI fraud prediction
        fraud_result = predict_fraud(permissions)
        fraud_prob = fraud_result['fraud_probability']
        risk_level = fraud_result['risk_level']

        # Combined score
        final_score = round((perm_score * 0.6 + fraud_prob * 0.4), 2)

        # Save LoanApp
        loan_app = LoanApp.objects.create(
            uploaded_by=request.user,
            app_name=app_name,
            package_name=package,
            risk_score=final_score,
            risk_level=risk_level.lower().replace(' ', '_').replace('medium_risk', 'medium'),
            fraud_probability=fraud_prob,
            total_permissions=len(permissions),
            dangerous_permissions_count=sum(
                1 for p in permissions if p['risk_level'] == 'high'
            ),
        )

        # Save permissions
        for p in permissions:
            Permission.objects.create(
                app=loan_app,
                permission_name=p['name'],
                risk_level=p['risk_level'],
                description=p['description'],
            )

        # NLP review analysis
        review_results = []
        if reviews_text.strip():
            reviews = [r.strip() for r in reviews_text.split('\n') if r.strip()]
            review_results = analyze_reviews_bulk(reviews, loan_app)

        return redirect('scan_result', pk=loan_app.pk)

    return render(request, 'apk_analysis/upload.html')


@login_required
def scan_result_view(request, pk):
    loan_app = get_object_or_404(LoanApp, pk=pk, uploaded_by=request.user)
    permissions = loan_app.permissions.all().order_by('-risk_level')
    reviews = loan_app.reviews.all() if hasattr(loan_app, 'reviews') else []
    context = {
        'app': loan_app,
        'permissions': permissions,
        'reviews': reviews,
        'high_perms': permissions.filter(risk_level='high'),
        'medium_perms': permissions.filter(risk_level='medium'),
        'low_perms': permissions.filter(risk_level='low'),
    }
    return render(request, 'apk_analysis/result.html', context)


@login_required
def history_view(request):
    apps = LoanApp.objects.filter(uploaded_by=request.user)
    return render(request, 'apk_analysis/history.html', {'apps': apps})


@login_required
def dashboard_view(request):
    user_apps = LoanApp.objects.filter(uploaded_by=request.user)
    total = user_apps.count()
    safe = user_apps.filter(risk_level='safe').count()
    medium = user_apps.filter(risk_level='medium').count()
    dangerous = user_apps.filter(risk_level='dangerous').count()
    recent = user_apps[:5]
    context = {
        'total': total,
        'safe': safe,
        'medium': medium,
        'dangerous': dangerous,
        'recent': recent,
    }
    return render(request, 'apk_analysis/dashboard.html', context)
