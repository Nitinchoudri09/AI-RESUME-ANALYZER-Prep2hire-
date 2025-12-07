from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.CharField(max_length=200, blank=True)  # URL or path to preview
    template_type = models.CharField(max_length=50, default='modern')  # modern, classic, creative, minimal, professional
    html_template = models.TextField()  # HTML template with placeholders
    css_styles = models.TextField()  # CSS for the template
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    resume_data = models.TextField()  # JSON data with resume information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_resume_data(self):
        try:
            return json.loads(self.resume_data)
        except:
            return {}
    
    def set_resume_data(self, data):
        self.resume_data = json.dumps(data)
    
    def __str__(self):
        return f"Resume by {self.user.username if self.user else 'Anonymous'} - {self.template.name}"
