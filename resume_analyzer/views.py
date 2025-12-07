from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import ResumeForm, ResumeBuilderForm
from .models import ResumeTemplate, UserResume
from .utils import extract_text
from .ai import calculate_similarity, missing_keywords, generate_suggestions
import json

def replace_template_placeholders(template_html, resume_data):
    """Helper function to replace placeholders in template HTML with resume data"""
    if not resume_data:
        return template_html
    
    personal_info = resume_data.get('personal_info', {})
    template_html = template_html.replace('{{full_name}}', personal_info.get('full_name', ''))
    template_html = template_html.replace('{{email}}', personal_info.get('email', ''))
    template_html = template_html.replace('{{phone}}', personal_info.get('phone', ''))
    template_html = template_html.replace('{{address}}', personal_info.get('address', ''))
    linkedin = personal_info.get('linkedin', '')
    github = personal_info.get('github', '')
    website = personal_info.get('website', '')
    address = personal_info.get('address', '')
    
    # Handle LinkedIn
    if linkedin:
        template_html = template_html.replace('{{linkedin}}', f'<a href="{linkedin}">LinkedIn</a>')
        template_html = template_html.replace('<span id="linkedin-link"></span>', f'<span>🔗 <a href="{linkedin}">LinkedIn</a></span>')
        template_html = template_html.replace('<span id="linkedin-link2"></span>', f'<span>🔗 <a href="{linkedin}">LinkedIn</a></span>')
    else:
        template_html = template_html.replace('{{linkedin}}', '')
        template_html = template_html.replace('<span id="linkedin-link"></span>', '')
        template_html = template_html.replace('<span id="linkedin-link2"></span>', '')
    
    # Handle GitHub
    if github:
        template_html = template_html.replace('{{github}}', f'<a href="{github}">GitHub</a>')
        template_html = template_html.replace('<span id="github-link"></span>', f'<span> | <a href="{github}">GitHub</a></span>')
        template_html = template_html.replace('<span id="github-link2"></span>', f'<span>💻 <a href="{github}">GitHub</a></span>')
    else:
        template_html = template_html.replace('{{github}}', '')
        template_html = template_html.replace('<span id="github-link"></span>', '')
        template_html = template_html.replace('<span id="github-link2"></span>', '')
    
    # Handle website
    template_html = template_html.replace('{{website}}', website)
    
    # Handle address
    if address:
        template_html = template_html.replace('<p id="address-line"></p>', f'<p>{address}</p>')
    else:
        template_html = template_html.replace('<p id="address-line"></p>', '')
    template_html = template_html.replace('{{summary}}', resume_data.get('summary', ''))
    
    # Education
    education_html = ''
    for edu in resume_data.get('education', []):
        education_html += f'<div class="education-item"><h4>{edu.get("degree", "")}</h4><p>{edu.get("institution", "")} - {edu.get("year", "")}'
        if edu.get('gpa'):
            education_html += f' | GPA: {edu.get("gpa")}'
        education_html += '</p></div>'
    template_html = template_html.replace('{{education}}', education_html)
    
    # Experience
    experience_html = ''
    for exp in resume_data.get('experience', []):
        experience_html += f'<div class="experience-item"><h4>{exp.get("title", "")} - {exp.get("company", "")}</h4>'
        experience_html += f'<p class="date">{exp.get("start", "")} - {exp.get("end", "")}</p>'
        experience_html += f'<p>{exp.get("description", "")}</p></div>'
    template_html = template_html.replace('{{experience}}', experience_html)
    
    # Skills
    skills_html = ', '.join(resume_data.get('skills', []))
    template_html = template_html.replace('{{skills}}', skills_html)
    
    # Projects
    projects_html = ''
    for proj in resume_data.get('projects', []):
        projects_html += f'<div class="project-item"><h4>{proj.get("name", "")}</h4>'
        projects_html += f'<p><strong>Technologies:</strong> {proj.get("technologies", "")}</p>'
        projects_html += f'<p>{proj.get("description", "")}</p>'
        if proj.get('link'):
            projects_html += f'<a href="{proj.get("link")}" target="_blank">View Project</a>'
        projects_html += '</div>'
    template_html = template_html.replace('{{projects}}', projects_html)
    
    return template_html

def analyze_resume(request):
    score = None
    suggestions = []
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['resume']
            job_desc = form.cleaned_data['job_description']
            resume_text = extract_text(resume_file)

            score = calculate_similarity(resume_text, job_desc)
            missing_words = missing_keywords(resume_text, job_desc)
            suggestions = generate_suggestions(missing_words)
    else:
        form = ResumeForm()
    
    return render(request, "analyze.html", {
        "form": form,
        "score": score,
        "suggestions": suggestions
    })

def resume_templates(request):
    """List all available resume templates"""
    templates = ResumeTemplate.objects.filter(is_active=True)
    return render(request, "resume_templates.html", {
        "templates": templates
    })

def create_resume(request, template_id):
    """Create a new resume using a selected template"""
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True)
    
    if request.method == "POST":
        # Get form data
        resume_data = {
            'personal_info': {
                'full_name': request.POST.get('full_name', ''),
                'email': request.POST.get('email', ''),
                'phone': request.POST.get('phone', ''),
                'address': request.POST.get('address', ''),
                'linkedin': request.POST.get('linkedin', ''),
                'github': request.POST.get('github', ''),
                'website': request.POST.get('website', ''),
            },
            'summary': request.POST.get('summary', ''),
            'education': json.loads(request.POST.get('education', '[]')),
            'experience': json.loads(request.POST.get('experience', '[]')),
            'skills': json.loads(request.POST.get('skills', '[]')),
            'projects': json.loads(request.POST.get('projects', '[]')),
        }
        
        # Save resume
        user_resume = UserResume.objects.create(
            user=request.user if request.user.is_authenticated else None,
            template=template
        )
        user_resume.set_resume_data(resume_data)
        user_resume.save()
        
        return redirect('resume_analyzer:preview_resume', resume_id=user_resume.id)
    
    return render(request, "create_resume.html", {
        "template": template
    })

def preview_resume(request, resume_id):
    """Preview the created resume"""
    resume = get_object_or_404(UserResume, id=resume_id)
    resume_data = resume.get_resume_data()
    
    # Replace placeholders in template HTML
    template_html = replace_template_placeholders(resume.template.html_template, resume_data)
    
    return render(request, "preview_resume.html", {
        "resume": resume,
        "resume_data": resume_data,
        "template_html": template_html,
        "template_css": resume.template.css_styles
    })

def download_resume_html(request, resume_id):
    """Download resume as HTML file"""
    resume = get_object_or_404(UserResume, id=resume_id)
    resume_data = resume.get_resume_data()
    
    # Replace placeholders in template HTML
    template_html = replace_template_placeholders(resume.template.html_template, resume_data)
    
    # Create full HTML document
    full_name = resume_data.get('personal_info', {}).get('full_name', 'Resume') if resume_data else 'Resume'
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{full_name} - Resume</title>
    <style>
        {resume.template.css_styles}
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
            }}
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    {template_html}
</body>
</html>'''
    
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{full_name.replace(" ", "_")}_Resume.html"'
    return response
