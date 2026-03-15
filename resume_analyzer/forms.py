from django import forms

class ResumeForm(forms.Form):
    resume = forms.FileField()
    job_description = forms.CharField(widget=forms.Textarea)

class ResumeBuilderForm(forms.Form):
    # Personal Information
    full_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=300, required=False)
    linkedin = forms.URLField(required=False)
    github = forms.URLField(required=False)
    website = forms.URLField(required=False)
    
    # Professional Summary
    summary = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    # Education (will be handled as JSON)
    # Experience (will be handled as JSON)
    # Skills (will be handled as JSON)
    # Projects (will be handled as JSON)