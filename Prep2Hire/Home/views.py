from django.shortcuts import render, redirect
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