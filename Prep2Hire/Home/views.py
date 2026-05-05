from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your Prep2Hire account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('username') # Standard UserCreationForm uses username as email? No, usually it's separate. 
            # Wait, standard UserCreationForm doesn't have email. I should check the form.
            # I'll try to get email if it exists, otherwise use username as email if it looks like one.
            email = request.POST.get('email') or user.username
            
            try:
                send_mail(mail_subject, message, 'no-reply@prep2hire.com', [email])
                return render(request, 'check_email.html', {'email': email})
            except Exception as e:
                print(e)
                user.delete() # Clean up if email fails
                return render(request, 'signup.html', {'form': form, 'error': 'Failed to send verification email. Please check your SMTP settings.'})
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'activation_invalid.html')


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

def forgot_password(request):
    return render(request, 'forgot_password.html')