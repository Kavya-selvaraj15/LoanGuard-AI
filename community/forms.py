from django import forms
from .models import ScamReport

class ScamReportForm(forms.ModelForm):
    class Meta:
        model = ScamReport
        fields = ['app_name', 'package_name', 'description', 'screenshot']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'app_name': forms.TextInput(attrs={'class': 'form-input'}),
            'package_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
