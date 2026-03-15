# admin.py
from django.contrib import admin
from .models import Question, Option, CareerSuggestion, Post, Like, MockInterview, InterviewQuestion, InterviewResponse, TestCategory, TestQuestion, TestOption, TestAttempt, TestResponse

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(CareerSuggestion)
admin.site.register(Post)
admin.site.register(Like)

@admin.register(MockInterview)
class MockInterviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_role', 'status', 'overall_rating', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'job_role']

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['interview', 'question_number', 'question_text']
    list_filter = ['interview']
    search_fields = ['question_text']

@admin.register(InterviewResponse)
class InterviewResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['answer_text', 'feedback']

from .models import TestCategory, TestQuestion, TestOption, TestAttempt, TestResponse

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name', 'description']

class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 4
    max_num = 4

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ['category', 'question_text', 'difficulty']
    list_filter = ['category', 'difficulty']
    search_fields = ['question_text']
    inlines = [TestOptionInline]

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'score', 'total_questions', 'percentage', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['user__username', 'category__name']

@admin.register(TestResponse)
class TestResponseAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct']
    list_filter = ['is_correct', 'attempt__category']
    search_fields = ['question__question_text']
