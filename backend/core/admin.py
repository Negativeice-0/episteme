from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

class EpistemeAdminSite(AdminSite):
    site_header = "Episteme Administration"
    site_title = "Episteme Admin"
    index_title = "Welcome to Episteme Control Panel"
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add custom stats to dashboard
        extra_context['stats'] = {
            'datasets': self._get_dataset_stats(),
            'models': self._get_model_stats(),
            'prompts': self._get_prompt_stats(),
        }
        
        return super().index(request, extra_context=extra_context)
    
    def _get_dataset_stats(self):
        from datasets.models import Dataset
        return {
            'total': Dataset.objects.count(),
            'active': Dataset.objects.filter(is_active=True).count(),
        }
    
    def _get_model_stats(self):
        # Add model training stats here later
        return {'trained': 3, 'pending': 0}
    
    def _get_prompt_stats(self):
        from socratic.models import Prompt
        return {
            'total': Prompt.objects.count(),
            'reflections': 0,  # Add later
        }

# Replace default admin site
admin_site = EpistemeAdminSite(name='admin')