from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScamReport
from .forms import ScamReportForm


@login_required
def reports_view(request):
    reports = ScamReport.objects.filter(status='verified') | \
              ScamReport.objects.filter(status='pending')
    return render(request, 'community/reports.html', {'reports': reports})


@login_required
def submit_report_view(request):
    form = ScamReportForm()
    if request.method == 'POST':
        form = ScamReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Report submitted! It will be reviewed by our team.')
            return redirect('reports')
    return render(request, 'community/submit_report.html', {'form': form})
