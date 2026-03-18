from django.contrib import admin
from .models import TrainedModel

@admin.register(TrainedModel)
class TrainedModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset', 'metrics_summary', 'is_active', 'trained_at']
    list_filter = ['name', 'dataset', 'is_active', 'trained_at']
    search_fields = ['dataset__name']
    readonly_fields = ['trained_at']
    
    def metrics_summary(self, obj):
        if obj.metrics:
            return f"R²: {obj.metrics.get('r2', 'N/A')}, RMSE: {obj.metrics.get('rmse', 'N/A')}"
        return "No metrics"
    metrics_summary.short_description = "Metrics"