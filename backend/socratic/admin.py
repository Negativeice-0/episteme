from django.contrib import admin
from .models import Prompt, Reflection

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'context', 'order', 'is_active', 'created_at']
    list_filter = ['context', 'is_active', 'created_at']
    search_fields = ['question', 'reflection_guide']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Prompt', {
            'fields': ('question', 'context', 'reflection_guide', 'order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_short(self, obj):
        return obj.question[:50] + ('...' if len(obj.question) > 50 else '')
    question_short.short_description = "Question"

@admin.register(Reflection)
class ReflectionAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'content_short', 'session_id', 'created_at']
    list_filter = ['prompt', 'created_at']
    search_fields = ['content', 'session_id']
    readonly_fields = ['created_at']
    
    def content_short(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_short.short_description = "Reflection"