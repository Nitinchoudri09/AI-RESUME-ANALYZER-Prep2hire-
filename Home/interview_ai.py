"""
AI functions for generating interview questions and providing feedback
"""
import random

# Pre-defined question templates based on job roles
QUESTION_TEMPLATES = {
    'software engineer': [
        "Tell me about yourself and your experience in software development.",
        "What programming languages are you most comfortable with? Can you give examples of projects where you used them?",
        "Describe a challenging technical problem you solved. What was your approach?",
        "How do you handle debugging and troubleshooting in your code?",
        "Explain a time when you had to learn a new technology quickly for a project.",
        "How do you ensure code quality and maintainability in your projects?",
        "Describe your experience with version control systems like Git.",
        "How do you approach testing your code? What testing strategies do you use?",
    ],
    'data scientist': [
        "Tell me about your experience with data analysis and machine learning.",
        "What machine learning algorithms are you familiar with? When would you use each?",
        "Describe a data science project you worked on. What was the problem and your solution?",
        "How do you handle missing or incomplete data in your analysis?",
        "Explain your experience with data visualization tools.",
        "What's your approach to feature engineering?",
        "Describe a time when you had to explain complex data insights to non-technical stakeholders.",
    ],
    'product manager': [
        "Tell me about yourself and your experience in product management.",
        "How do you prioritize features for a product?",
        "Describe a product you managed from conception to launch.",
        "How do you gather and analyze user feedback?",
        "Explain your approach to working with engineering and design teams.",
        "How do you define and measure product success?",
        "Describe a time when you had to make a difficult product decision.",
    ],
    'web developer': [
        "Tell me about your experience with web development.",
        "What frontend and backend technologies are you most familiar with?",
        "Describe a web application you built. What technologies did you use?",
        "How do you ensure your web applications are responsive and accessible?",
        "Explain your experience with APIs and RESTful services.",
        "How do you optimize website performance?",
        "Describe your experience with frontend frameworks like React, Vue, or Angular.",
    ],
    'default': [
        "Tell me about yourself and your background.",
        "Why are you interested in this role?",
        "What are your greatest strengths?",
        "Describe a challenging situation you faced at work and how you handled it.",
        "Where do you see yourself in 5 years?",
        "How do you handle working under pressure?",
        "What motivates you in your work?",
        "Describe a time when you had to work in a team. What was your role?",
    ]
}

def generate_questions(job_role, num_questions=5):
    """Generate interview questions based on job role"""
    role_lower = job_role.lower()
    
    # Find matching questions
    questions = []
    for key, templates in QUESTION_TEMPLATES.items():
        if key in role_lower:
            questions = templates.copy()
            break
    
    # If no specific match, use default
    if not questions:
        questions = QUESTION_TEMPLATES['default'].copy()
    
    # Select random questions
    if len(questions) == 0:
        return []
    
    num_to_select = min(num_questions, len(questions))
    if num_to_select == len(questions):
        # If we want all questions, just shuffle and return
        selected = questions.copy()
        random.shuffle(selected)
    else:
        # Select random subset
        selected = random.sample(questions, num_to_select)
    
    return selected

def analyze_answer(question, answer, job_role):
    """Analyze answer and provide feedback, rating, strengths, and improvements"""
    answer_lower = answer.lower()
    answer_length = len(answer.split())
    
    # Basic analysis
    rating = 5.0  # Base rating
    feedback_parts = []
    strengths = []
    improvements = []
    
    # Length analysis
    if answer_length < 20:
        rating -= 1.5
        improvements.append("Your answer is quite brief. Try to provide more detail and examples.")
    elif answer_length > 150:
        rating -= 0.5
        improvements.append("Your answer might be too long. Try to be more concise while covering key points.")
    else:
        strengths.append("Good answer length - detailed but concise.")
    
    # Check for examples
    example_keywords = ['example', 'instance', 'time when', 'project', 'experience', 'worked on']
    has_examples = any(keyword in answer_lower for keyword in example_keywords)
    if has_examples:
        rating += 1.0
        strengths.append("Good use of specific examples and experiences.")
    else:
        improvements.append("Try to include specific examples from your experience.")
    
    # Check for technical terms (for technical roles)
    if any(term in job_role.lower() for term in ['engineer', 'developer', 'scientist', 'technical']):
        tech_keywords = ['code', 'algorithm', 'system', 'design', 'architecture', 'framework', 'api', 'database']
        has_tech = any(keyword in answer_lower for keyword in tech_keywords)
        if has_tech:
            rating += 0.5
            strengths.append("Good use of technical terminology.")
        else:
            improvements.append("Consider using more technical terms relevant to the role.")
    
    # Check for problem-solving approach
    if 'problem' in question.lower() or 'challenge' in question.lower():
        approach_keywords = ['approach', 'method', 'strategy', 'solution', 'steps', 'process']
        has_approach = any(keyword in answer_lower for keyword in approach_keywords)
        if has_approach:
            rating += 1.0
            strengths.append("Good explanation of your problem-solving approach.")
        else:
            improvements.append("Try to explain your thought process and approach more clearly.")
    
    # Check for STAR method elements (Situation, Task, Action, Result)
    star_keywords = ['situation', 'task', 'action', 'result', 'outcome', 'achieved']
    has_star = sum(1 for keyword in star_keywords if keyword in answer_lower)
    if has_star >= 2:
        rating += 0.5
        strengths.append("Good structure following STAR method principles.")
    
    # Ensure rating is within bounds
    rating = max(0.0, min(10.0, rating))
    
    # Generate feedback
    if rating >= 8.0:
        feedback_parts.append("Excellent answer! You demonstrated strong understanding and provided relevant examples.")
    elif rating >= 6.0:
        feedback_parts.append("Good answer with room for improvement.")
    elif rating >= 4.0:
        feedback_parts.append("Your answer needs more detail and structure.")
    else:
        feedback_parts.append("Your answer needs significant improvement. Focus on providing specific examples and clearer explanations.")
    
    feedback = " ".join(feedback_parts)
    
    # Format strengths and improvements
    strengths_text = "\n".join(f"• {s}" for s in strengths) if strengths else "• Keep practicing to identify your strengths."
    improvements_text = "\n".join(f"• {i}" for i in improvements) if improvements else "• Continue to refine your answers."
    
    return {
        'rating': round(rating, 1),
        'feedback': feedback,
        'strengths': strengths_text,
        'improvements': improvements_text
    }

