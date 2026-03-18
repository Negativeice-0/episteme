from django.contrib import admin
from django.utils.html import format_html
from .models import Dataset, DataPoint

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'n_samples', 'n_features', 'is_active', 'created_at', 'data_preview']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'data_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'source', 'is_active')
        }),
        ('Data Structure', {
            'fields': ('features', 'feature_descriptions', 'target', 'units')
        }),
        ('Data', {
            'fields': ('data', 'data_preview'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def n_samples(self, obj):
        return obj.n_samples
    n_samples.short_description = "Samples"
    
    def n_features(self, obj):
        return obj.n_features
    n_features.short_description = "Features"
    
    def data_preview(self, obj):
        if obj.data and len(obj.data) > 0:
            import json
            preview = obj.data[:3]  # First 3 rows
            return format_html(
                '<pre style="background: #f8f9fa; padding: 10px; border-radius: 5px; max-height: 200px; overflow: auto;">{}</pre>',
                json.dumps(preview, indent=2)
            )
        return "No data"
    data_preview.short_description = "Data Preview"

@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'id', 'created_at']
    list_filter = ['dataset', 'created_at']
    search_fields = ['dataset__name']