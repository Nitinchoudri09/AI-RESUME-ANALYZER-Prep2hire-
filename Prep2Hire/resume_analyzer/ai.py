from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re
from collections import Counter
import spacy

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load spaCy for better NLP (fallback if not available)
try:
    nlp = spacy.load('en_core_web_sm')
except:
    nlp = None

# Common technical skills and job-related terms
TECHNICAL_SKILLS = {
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php',
    'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'express',
    'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
    'machine learning', 'deep learning', 'nlp', 'data science', 'ai', 'tensorflow',
    'pytorch', 'scikit-learn', 'pandas', 'numpy', 'spark', 'hadoop',
    'agile', 'scrum', 'kanban', 'devops', 'microservices', 'rest', 'graphql',
    'html', 'css', 'sass', 'typescript', 'webpack', 'babel', 'linux', 'unix'
}

def extract_keywords(text):
    """Extract meaningful keywords using NLP techniques"""
    if nlp:
        doc = nlp(text.lower())
        # Extract nouns, proper nouns, and adjectives that are likely skills
        keywords = []
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                not token.is_stop and 
                len(token.text) > 2 and
                token.text not in ENGLISH_STOP_WORDS):
                keywords.append(token.lemma_)
        
        # Extract named entities (organizations, technologies)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART']:
                keywords.append(ent.text.lower())
        
        return set(keywords)
    else:
        # Fallback to regex-based extraction
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        keywords = [w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 2]
        return set(keywords)

def extract_phrases(text):
    """Extract multi-word phrases and technical terms"""
    phrases = set()
    text_lower = text.lower()
    
    # Extract technical skills
    for skill in TECHNICAL_SKILLS:
        if skill in text_lower:
            phrases.add(skill)
    
    # Extract common patterns (e.g., "n years experience", "proficient in")
    exp_pattern = r'(\d+)\+?\s*(years?|months?)\s*(of\s*)?(experience|exp)'
    for match in re.finditer(exp_pattern, text_lower):
        phrases.add(match.group(0))
    
    # Extract degree patterns
    degree_pattern = r'(bachelor|master|phd|doctorate|b\.s\.|m\.s\.|b\.a\.|m\.a\.).*?(degree|in\s+\w+)'
    for match in re.finditer(degree_pattern, text_lower):
        phrases.add(match.group(0))
    
    return phrases

def calculate_ats_score(resume_text, job_desc):
    """Calculate comprehensive ATS score based on multiple factors"""
    # Extract keywords and phrases
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc)
    resume_phrases = extract_phrases(resume_text)
    jd_phrases = extract_phrases(job_desc)
    
    # 1. Keyword matching score (40% weight)
    if jd_keywords:
        keyword_match = len(resume_keywords & jd_keywords) / len(jd_keywords)
    else:
        keyword_match = 0
    
    # 2. Phrase/skill matching score (30% weight)
    if jd_phrases:
        phrase_match = len(resume_phrases & jd_phrases) / len(jd_phrases)
    else:
        phrase_match = 0
    
    # 3. Semantic similarity score (20% weight)
    embeddings = model.encode([resume_text, job_desc])
    semantic_score = util.cos_sim(embeddings[0], embeddings[1]).item()
    
    # 4. Length and completeness score (10% weight)
    resume_words = len(resume_text.split())
    length_score = min(resume_words / 500, 1.0)  # Ideal: 500+ words
    
    # Calculate weighted score
    ats_score = (
        keyword_match * 0.40 +
        phrase_match * 0.30 +
        semantic_score * 0.20 +
        length_score * 0.10
    ) * 100
    
    return round(ats_score, 2)

def calculate_similarity(resume_text, job_desc):
    """Legacy function - now uses ATS score"""
    return calculate_ats_score(resume_text, job_desc)

def missing_keywords(resume_text, job_desc):
    """Find missing keywords with categorization"""
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc)
    resume_phrases = extract_phrases(resume_text)
    jd_phrases = extract_phrases(job_desc)
    
    # Categorize missing keywords
    missing = {
        'technical': [],
        'soft_skills': [],
        'experience': [],
        'general': []
    }
    
    for word in (jd_keywords - resume_keywords):
        if word in TECHNICAL_SKILLS:
            missing['technical'].append(word)
        elif word in ['communication', 'teamwork', 'leadership', 'collaboration', 'problem-solving']:
            missing['soft_skills'].append(word)
        elif word in ['experience', 'years', 'worked', 'managed', 'led']:
            missing['experience'].append(word)
        else:
            missing['general'].append(word)
    
    # Add missing phrases
    for phrase in (jd_phrases - resume_phrases):
        if phrase not in [item for sublist in missing.values() for item in sublist]:
            missing['general'].append(phrase)
    
    return missing

def generate_suggestions(missing_keywords_dict):
    """Generate dynamic suggestions based on missing keywords"""
    suggestions = []
    
    # Technical skills suggestions
    if missing_keywords_dict['technical']:
        skills = ', '.join(missing_keywords_dict['technical'][:5])
        suggestions.append(f"Add these technical skills to your resume: {skills}. Consider taking online courses or certifications to gain these skills.")
    
    # Soft skills suggestions
    if missing_keywords_dict['soft_skills']:
        skills = ', '.join(missing_keywords_dict['soft_skills'])
        suggestions.append(f"Highlight your soft skills: {skills}. Provide specific examples of how you've demonstrated these in previous roles or projects.")
    
    # Experience suggestions
    if missing_keywords_dict['experience']:
        suggestions.append("Quantify your experience with specific metrics (e.g., 'Led a team of 5 developers', 'Improved performance by 30%'). Include years of experience for each role.")
    
    # General keyword suggestions
    if missing_keywords_dict['general']:
        top_general = missing_keywords_dict['general'][:5]
        suggestions.append(f"Incorporate these relevant terms: {', '.join(top_general)}. These keywords are important for ATS systems.")
    
    # If no missing keywords
    if not any(missing_keywords_dict.values()):
        suggestions.append("Great job! Your resume aligns well with the job description. Consider tailoring it further with specific achievements and metrics.")
    
    return suggestions
