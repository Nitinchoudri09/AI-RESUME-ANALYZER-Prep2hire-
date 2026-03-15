from django.shortcuts import render
from .forms import ResumeForm
from .utils import extract_text
from .ai import calculate_similarity, missing_keywords, generate_suggestions

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
