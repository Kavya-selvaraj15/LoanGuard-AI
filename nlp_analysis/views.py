from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def review_analysis_view(request):
    return render(request, 'nlp_analysis/reviews.html')
