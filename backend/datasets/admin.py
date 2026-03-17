from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'n_samples', 'n_features', 'is_active', 'created_at', 'preview_link']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'sample_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'source', 'is_active')
        }),
        ('Data Structure', {
            'fields': ('features', 'feature_descriptions', 'target', 'units')
        }),
        ('Statistics', {
            'fields': ('sample_data', 'sample_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def n_samples(self, obj):
        return len(obj.sample_data) if obj.sample_data else 0
    n_samples.short_description = "Samples"
    
    def n_features(self, obj):
        return len(obj.features) if obj.features else 0
    n_features.short_description = "Features"
    
    def sample_preview(self, obj):
        if obj.sample_data:
            import json
            return format_html(
                '<pre style="background: #f8f9fa; padding: 10px; border-radius: 5px;">{}</pre>',
                json.dumps(obj.sample_data[:3], indent=2)
            )
        return "No sample data"
    sample_preview.short_description = "Sample Preview"
    
    def preview_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank" style="background: #ffb347; color: #0a1929; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Preview Data</a>',
            reverse('dataset-preview', args=[obj.id])
        )
    preview_link.short_description = "Actions"