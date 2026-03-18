from django.db import models

class Prompt(models.Model):
    """Socratic learning prompts"""
    question = models.TextField()
    context = models.CharField(max_length=100, help_text="Topic area (e.g., 'crime', 'education')")
    reflection_guide = models.TextField(help_text="Guidance for reflection")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.question[:50]

class Reflection(models.Model):
    """User reflections on prompts"""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='reflections')
    content = models.TextField()
    session_id = models.CharField(max_length=100)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']