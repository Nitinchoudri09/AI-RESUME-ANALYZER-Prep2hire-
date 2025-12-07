from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import logout

class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt  # Optional if you want GET request (not recommended for delete)
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)         # Logs out the user
        user.delete()           # Deletes the user from DB
        return redirect('/')    # Redirect to homepage (or show a message)
    else:
        return redirect('/') 
    

from .models import Question, Option, CareerSuggestion

def career_quiz(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        scores = {}
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            if selected:
                option = Option.objects.get(id=selected)
                for career, val in option.score_map.items():
                    scores[career] = scores.get(career, 0) + val

        # Find top scoring career
        suggested_career = max(scores, key=scores.get)
        suggestion = CareerSuggestion.objects.get(career=suggested_career)
        return render(request, 'carreer_result.html', {'suggestion': suggestion})

    return render(request, 'career_quiz.html', {'questions': questions})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from .forms import PostForm

from .models import Post, Like

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.has_liked = post.likes.filter(user=request.user).exists()

    return render(request, 'connect/post_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'connect/post_form.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('post_list')

from django.http import JsonResponse

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False

    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.likes.count()
    })

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

from .models import MockInterview, InterviewQuestion, InterviewResponse, TestCategory, TestQuestion, TestOption, TestAttempt, TestResponse
from .interview_ai import generate_questions, analyze_answer
from django.utils import timezone
from django.http import JsonResponse
import random

@login_required
def start_interview(request):
    """Start a new mock interview"""
    if request.method == 'POST':
        job_role = request.POST.get('job_role', '').strip()
        if not job_role:
            return render(request, 'mock_interview/start.html', {
                'error': 'Please enter a job role.'
            })
        
        try:
            # Create new interview
            interview = MockInterview.objects.create(
                user=request.user,
                job_role=job_role,
                status='in_progress'
            )
            
            # Generate questions
            questions = generate_questions(job_role, num_questions=5)
            if not questions:
                interview.delete()
                return render(request, 'mock_interview/start.html', {
                    'error': 'Unable to generate questions. Please try again.'
                })
            
            for i, question_text in enumerate(questions, 1):
                InterviewQuestion.objects.create(
                    interview=interview,
                    question_text=question_text,
                    question_number=i
                )
            
            return redirect('interview', interview_id=interview.id)
        except Exception as e:
            return render(request, 'mock_interview/start.html', {
                'error': f'An error occurred: {str(e)}'
            })
    
    return render(request, 'mock_interview/start.html')

@login_required
def interview_view(request, interview_id):
    """Display interview questions and handle answers"""
    interview = get_object_or_404(MockInterview, id=interview_id, user=request.user)
    questions = interview.questions.all()
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer', '').strip()
        
        if question_id and answer_text:
            question = get_object_or_404(InterviewQuestion, id=question_id, interview=interview)
            
            # Analyze answer
            analysis = analyze_answer(question.question_text, answer_text, interview.job_role)
            
            # Save response
            response, created = InterviewResponse.objects.get_or_create(
                question=question,
                defaults={
                    'answer_text': answer_text,
                    'rating': analysis['rating'],
                    'feedback': analysis['feedback'],
                    'strengths': analysis['strengths'],
                    'improvements': analysis['improvements']
                }
            )
            
            if not created:
                response.answer_text = answer_text
                response.rating = analysis['rating']
                response.feedback = analysis['feedback']
                response.strengths = analysis['strengths']
                response.improvements = analysis['improvements']
                response.save()
            
            return JsonResponse({
                'success': True,
                'rating': analysis['rating'],
                'feedback': analysis['feedback'],
                'strengths': analysis['strengths'],
                'improvements': analysis['improvements']
            })
    
    # Get answered questions
    answered_questions = set(
        InterviewResponse.objects.filter(question__interview=interview)
        .values_list('question_id', flat=True)
    )
    
    return render(request, 'mock_interview/interview.html', {
        'interview': interview,
        'questions': questions,
        'answered_questions': answered_questions
    })

@login_required
def complete_interview(request, interview_id):
    """Complete interview and show results"""
    interview = get_object_or_404(MockInterview, id=interview_id, user=request.user)
    
    if request.method == 'POST':
        # Calculate overall rating
        responses = InterviewResponse.objects.filter(question__interview=interview)
        if responses.exists():
            avg_rating = sum(r.rating for r in responses if r.rating) / responses.count()
            interview.overall_rating = avg_rating
        else:
            interview.overall_rating = 0.0
        
        interview.status = 'completed'
        interview.completed_at = timezone.now()
        interview.save()
        
        return redirect('results', interview_id=interview.id)
    
    return redirect('mock_interview:interview', interview_id=interview.id)

@login_required
def interview_results(request, interview_id):
    """Show interview results"""
    interview = get_object_or_404(MockInterview, id=interview_id, user=request.user)
    responses = InterviewResponse.objects.filter(question__interview=interview).select_related('question')
    
    return render(request, 'mock_interview/results.html', {
        'interview': interview,
        'responses': responses
    })

@login_required
def interview_history(request):
    """Show user's interview history"""
    interviews = MockInterview.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mock_interview/history.html', {
        'interviews': interviews
    })

# Test Views
@login_required
def test_categories(request):
    """List all test categories"""
    categories = TestCategory.objects.all()
    return render(request, 'tests/categories.html', {
        'categories': categories
    })

@login_required
def start_test(request, category_id):
    """Start a test for a specific category"""
    category = get_object_or_404(TestCategory, id=category_id)
    
    # Get random questions (10 questions per test)
    all_questions = list(category.questions.all())
    if len(all_questions) < 10:
        questions = all_questions
    else:
        questions = random.sample(all_questions, 10)
    
    if request.method == 'POST':
        # Create test attempt
        attempt = TestAttempt.objects.create(
            user=request.user,
            category=category,
            total_questions=len(questions)
        )
        
        score = 0
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    selected_option = TestOption.objects.get(id=selected_option_id, question=question)
                    is_correct = selected_option.is_correct
                    if is_correct:
                        score += 1
                except TestOption.DoesNotExist:
                    is_correct = False
            else:
                is_correct = False
                selected_option = None
            
            TestResponse.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )
        
        # Update attempt score
        attempt.score = score
        attempt.percentage = (score / attempt.total_questions * 100) if attempt.total_questions > 0 else 0
        attempt.save()
        
        return redirect('test_results', attempt_id=attempt.id)
    
    # Shuffle options for each question
    for question in questions:
        question.shuffled_options = list(question.options.all())
        random.shuffle(question.shuffled_options)
    
    return render(request, 'tests/take_test.html', {
        'category': category,
        'questions': questions
    })

@login_required
def test_results(request, attempt_id):
    """Show test results"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    responses = attempt.responses.all().select_related('question', 'selected_option')
    
    return render(request, 'tests/results.html', {
        'attempt': attempt,
        'responses': responses
    })

@login_required
def test_history(request):
    """Show user's test history"""
    attempts = TestAttempt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tests/history.html', {
        'attempts': attempts
    })