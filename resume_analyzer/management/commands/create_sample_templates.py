from django.core.management.base import BaseCommand
from resume_analyzer.models import ResumeTemplate

class Command(BaseCommand):
    help = 'Creates sample resume templates'

    def handle(self, *args, **options):
        templates_data = [
            {
                'name': 'Modern Professional',
                'description': 'Clean and modern design perfect for tech professionals',
                'template_type': 'modern',
                'html_template': '''
                    <div class="resume-modern">
                        <div class="header">
                            <h1>{{full_name}}</h1>
                            <div class="contact-info">
                                <span>{{email}}</span> | <span>{{phone}}</span> | <span>{{address}}</span>
                                {% if linkedin %}<span> | <a href="{{linkedin}}">LinkedIn</a></span>{% endif %}
                                {% if github %}<span> | <a href="{{github}}">GitHub</a></span>{% endif %}
                            </div>
                        </div>
                        <div class="section">
                            <h2>Professional Summary</h2>
                            <p>{{summary}}</p>
                        </div>
                        <div class="section">
                            <h2>Education</h2>
                            {{education}}
                        </div>
                        <div class="section">
                            <h2>Experience</h2>
                            {{experience}}
                        </div>
                        <div class="section">
                            <h2>Skills</h2>
                            <p>{{skills}}</p>
                        </div>
                        <div class="section">
                            <h2>Projects</h2>
                            {{projects}}
                        </div>
                    </div>
                ''',
                'css_styles': '''
                    .resume-modern {
                        font-family: 'Arial', sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }
                    .resume-modern .header {
                        text-align: center;
                        border-bottom: 3px solid #667eea;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }
                    .resume-modern .header h1 {
                        color: #667eea;
                        margin-bottom: 10px;
                    }
                    .resume-modern .section {
                        margin-bottom: 30px;
                    }
                    .resume-modern .section h2 {
                        color: #667eea;
                        border-bottom: 2px solid #e0e0e0;
                        padding-bottom: 5px;
                    }
                    .resume-modern .education-item,
                    .resume-modern .experience-item,
                    .resume-modern .project-item {
                        margin-bottom: 20px;
                    }
                    .resume-modern .date {
                        color: #666;
                        font-style: italic;
                    }
                '''
            },
            {
                'name': 'Classic Elegant',
                'description': 'Traditional and elegant design for corporate positions',
                'template_type': 'classic',
                'html_template': '''
                    <div class="resume-classic">
                        <div class="header">
                            <h1>{{full_name}}</h1>
                            <p>{{email}} | {{phone}} | {{address}}</p>
                        </div>
                        <div class="section">
                            <h2>SUMMARY</h2>
                            <p>{{summary}}</p>
                        </div>
                        <div class="section">
                            <h2>EDUCATION</h2>
                            {{education}}
                        </div>
                        <div class="section">
                            <h2>PROFESSIONAL EXPERIENCE</h2>
                            {{experience}}
                        </div>
                        <div class="section">
                            <h2>SKILLS</h2>
                            <p>{{skills}}</p>
                        </div>
                        <div class="section">
                            <h2>PROJECTS</h2>
                            {{projects}}
                        </div>
                    </div>
                ''',
                'css_styles': '''
                    .resume-classic {
                        font-family: 'Times New Roman', serif;
                        line-height: 1.8;
                    }
                    .resume-classic .header {
                        text-align: center;
                        margin-bottom: 30px;
                    }
                    .resume-classic .header h1 {
                        font-size: 24px;
                        text-transform: uppercase;
                        letter-spacing: 2px;
                    }
                    .resume-classic .section h2 {
                        text-transform: uppercase;
                        font-size: 14px;
                        letter-spacing: 1px;
                        border-bottom: 1px solid #000;
                        padding-bottom: 5px;
                    }
                '''
            },
            {
                'name': 'Creative Designer',
                'description': 'Bold and creative design for designers and creatives',
                'template_type': 'creative',
                'html_template': '''
                    <div class="resume-creative">
                        <div class="header">
                            <h1>{{full_name}}</h1>
                            <div class="contact">{{email}} • {{phone}} • {{address}}</div>
                        </div>
                        <div class="section">
                            <h2>About</h2>
                            <p>{{summary}}</p>
                        </div>
                        <div class="section">
                            <h2>Education</h2>
                            {{education}}
                        </div>
                        <div class="section">
                            <h2>Work Experience</h2>
                            {{experience}}
                        </div>
                        <div class="section">
                            <h2>Skills</h2>
                            <p>{{skills}}</p>
                        </div>
                        <div class="section">
                            <h2>Portfolio</h2>
                            {{projects}}
                        </div>
                    </div>
                ''',
                'css_styles': '''
                    .resume-creative {
                        font-family: 'Helvetica', sans-serif;
                        background: #fff;
                    }
                    .resume-creative .header {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 40px;
                        margin: -40px -40px 30px -40px;
                    }
                    .resume-creative .header h1 {
                        font-size: 36px;
                        margin-bottom: 10px;
                    }
                    .resume-creative .section h2 {
                        color: #667eea;
                        font-size: 20px;
                        margin-bottom: 15px;
                    }
                '''
            },
            {
                'name': 'Minimal Clean',
                'description': 'Simple and minimal design focusing on content',
                'template_type': 'minimal',
                'html_template': '''
                    <div class="resume-minimal">
                        <div class="header">
                            <h1>{{full_name}}</h1>
                            <p>{{email}} • {{phone}}</p>
                            <p id="address-line"></p>
                        </div>
                        <div class="section">
                            <h2>Summary</h2>
                            <p>{{summary}}</p>
                        </div>
                        <div class="section">
                            <h2>Education</h2>
                            {{education}}
                        </div>
                        <div class="section">
                            <h2>Experience</h2>
                            {{experience}}
                        </div>
                        <div class="section">
                            <h2>Skills</h2>
                            <p>{{skills}}</p>
                        </div>
                        <div class="section">
                            <h2>Projects</h2>
                            {{projects}}
                        </div>
                    </div>
                ''',
                'css_styles': '''
                    .resume-minimal {
                        font-family: 'Georgia', serif;
                        line-height: 1.8;
                    }
                    .resume-minimal .header {
                        margin-bottom: 40px;
                    }
                    .resume-minimal .header h1 {
                        font-size: 28px;
                        font-weight: normal;
                        margin-bottom: 5px;
                    }
                    .resume-minimal .section {
                        margin-bottom: 25px;
                    }
                    .resume-minimal .section h2 {
                        font-size: 16px;
                        font-weight: normal;
                        text-transform: lowercase;
                        margin-bottom: 10px;
                    }
                '''
            },
            {
                'name': 'Tech Professional',
                'description': 'Designed specifically for software engineers and developers',
                'template_type': 'professional',
                'html_template': '''
                    <div class="resume-tech">
                        <div class="header">
                            <h1>{{full_name}}</h1>
                            <div class="contact">
                                <span>📧 {{email}}</span>
                                <span>📱 {{phone}}</span>
                                <span id="linkedin-link2"></span>
                                <span id="github-link2"></span>
                            </div>
                        </div>
                        <div class="section">
                            <h2>Summary</h2>
                            <p>{{summary}}</p>
                        </div>
                        <div class="section">
                            <h2>Education</h2>
                            {{education}}
                        </div>
                        <div class="section">
                            <h2>Experience</h2>
                            {{experience}}
                        </div>
                        <div class="section">
                            <h2>Technical Skills</h2>
                            <p>{{skills}}</p>
                        </div>
                        <div class="section">
                            <h2>Projects</h2>
                            {{projects}}
                        </div>
                    </div>
                ''',
                'css_styles': '''
                    .resume-tech {
                        font-family: 'Courier New', monospace;
                        background: #f8f9fa;
                    }
                    .resume-tech .header {
                        background: #2d3748;
                        color: white;
                        padding: 30px;
                        margin: -40px -40px 30px -40px;
                    }
                    .resume-tech .header h1 {
                        color: #48bb78;
                        margin-bottom: 15px;
                    }
                    .resume-tech .section {
                        background: white;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-left: 4px solid #48bb78;
                    }
                    .resume-tech .section h2 {
                        color: #2d3748;
                        margin-bottom: 15px;
                    }
                '''
            },
            {
                'name': 'Executive Style',
                'description': 'Professional design for executives and senior positions',
                'template_type': 'professional',
                'html_template': '''
                    <div class="resume-executive">
                        <div class="header">
                            <h1>{{full_name}}</h1>
                            <p class="contact">{{email}} | {{phone}} | {{address}}</p>
                        </div>
                        <div class="section">
                            <h2>Executive Summary</h2>
                            <p>{{summary}}</p>
                        </div>
                        <div class="section">
                            <h2>Education</h2>
                            {{education}}
                        </div>
                        <div class="section">
                            <h2>Professional Experience</h2>
                            {{experience}}
                        </div>
                        <div class="section">
                            <h2>Core Competencies</h2>
                            <p>{{skills}}</p>
                        </div>
                        <div class="section">
                            <h2>Key Projects</h2>
                            {{projects}}
                        </div>
                    </div>
                ''',
                'css_styles': '''
                    .resume-executive {
                        font-family: 'Arial', sans-serif;
                        line-height: 1.7;
                    }
                    .resume-executive .header {
                        text-align: center;
                        border-bottom: 4px double #000;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }
                    .resume-executive .header h1 {
                        font-size: 32px;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                    .resume-executive .section {
                        margin-bottom: 25px;
                    }
                    .resume-executive .section h2 {
                        font-size: 18px;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        margin-bottom: 15px;
                        border-bottom: 2px solid #333;
                        padding-bottom: 5px;
                    }
                '''
            }
        ]
        
        for template_data in templates_data:
            template, created = ResumeTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created template: {template_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Template already exists: {template_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('Sample templates created successfully!'))

