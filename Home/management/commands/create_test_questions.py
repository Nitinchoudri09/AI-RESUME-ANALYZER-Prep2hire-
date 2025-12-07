from django.core.management.base import BaseCommand
from Home.models import TestCategory, TestQuestion, TestOption

class Command(BaseCommand):
    help = 'Creates sample test questions for Aptitude, Logical Reasoning, and English Grammar'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Aptitude Test',
                'description': 'Test your mathematical and analytical skills',
                'icon': 'fa-calculator'
            },
            {
                'name': 'Logical Reasoning',
                'description': 'Enhance your logical thinking and problem-solving abilities',
                'icon': 'fa-brain'
            },
            {
                'name': 'English Grammar',
                'description': 'Improve your English grammar and language skills',
                'icon': 'fa-book'
            }
        ]
        
        for cat_data in categories_data:
            category, created = TestCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_data["name"]}'))
            
            # Create questions based on category
            if category.name == 'Aptitude Test':
                self.create_aptitude_questions(category)
            elif category.name == 'Logical Reasoning':
                self.create_logical_reasoning_questions(category)
            elif category.name == 'English Grammar':
                self.create_english_grammar_questions(category)
        
        self.stdout.write(self.style.SUCCESS('Test questions created successfully!'))
    
    def create_aptitude_questions(self, category):
        questions_data = [
            {
                'question': 'If 15% of a number is 45, what is 30% of that number?',
                'options': ['60', '90', '120', '150'],
                'correct': 1,
                'explanation': 'If 15% = 45, then 1% = 3, so 30% = 90'
            },
            {
                'question': 'A train travels 240 km in 3 hours. What is its average speed?',
                'options': ['60 km/h', '70 km/h', '80 km/h', '90 km/h'],
                'correct': 2,
                'explanation': 'Speed = Distance/Time = 240/3 = 80 km/h'
            },
            {
                'question': 'What is the square root of 144?',
                'options': ['10', '11', '12', '13'],
                'correct': 2,
                'explanation': '12 × 12 = 144, so √144 = 12'
            },
            {
                'question': 'If the ratio of boys to girls in a class is 3:2 and there are 30 students, how many girls are there?',
                'options': ['10', '12', '15', '18'],
                'correct': 1,
                'explanation': 'Total parts = 3+2 = 5. Girls = (2/5) × 30 = 12'
            },
            {
                'question': 'A shopkeeper sells an item for $120 and makes a profit of 20%. What was the cost price?',
                'options': ['$90', '$100', '$110', '$115'],
                'correct': 1,
                'explanation': 'If CP = x, then 1.2x = 120, so x = 100'
            },
            {
                'question': 'What is 25% of 200?',
                'options': ['40', '50', '60', '75'],
                'correct': 1,
                'explanation': '25% of 200 = (25/100) × 200 = 50'
            },
            {
                'question': 'If a number is increased by 20% and then decreased by 20%, what is the net change?',
                'options': ['No change', '4% decrease', '4% increase', '20% decrease'],
                'correct': 1,
                'explanation': 'Let x be the number. After 20% increase: 1.2x. After 20% decrease: 0.8 × 1.2x = 0.96x. Net change = 4% decrease'
            },
            {
                'question': 'What is the LCM of 12 and 18?',
                'options': ['24', '36', '48', '54'],
                'correct': 1,
                'explanation': 'LCM of 12 and 18 = 36'
            },
            {
                'question': 'A rectangle has length 8 cm and width 6 cm. What is its area?',
                'options': ['42 cm²', '48 cm²', '52 cm²', '56 cm²'],
                'correct': 1,
                'explanation': 'Area = length × width = 8 × 6 = 48 cm²'
            },
            {
                'question': 'If 3x + 5 = 20, what is the value of x?',
                'options': ['3', '4', '5', '6'],
                'correct': 2,
                'explanation': '3x + 5 = 20, so 3x = 15, therefore x = 5'
            }
        ]
        self.create_questions(category, questions_data)
    
    def create_logical_reasoning_questions(self, category):
        questions_data = [
            {
                'question': 'If all roses are flowers and some flowers are red, which statement must be true?',
                'options': ['All roses are red', 'Some roses are red', 'No roses are red', 'Cannot be determined'],
                'correct': 3,
                'explanation': 'We cannot determine if roses are red from the given information'
            },
            {
                'question': 'Complete the series: 2, 6, 12, 20, 30, ?',
                'options': ['40', '42', '44', '46'],
                'correct': 1,
                'explanation': 'The pattern is: 1×2, 2×3, 3×4, 4×5, 5×6, so next is 6×7 = 42'
            },
            {
                'question': 'If Monday is the first day, what day will it be 25 days later?',
                'options': ['Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'correct': 2,
                'explanation': '25 days = 3 weeks + 4 days. Monday + 4 days = Friday'
            },
            {
                'question': 'A is taller than B, B is taller than C. Who is the shortest?',
                'options': ['A', 'B', 'C', 'Cannot be determined'],
                'correct': 2,
                'explanation': 'A > B > C, so C is the shortest'
            },
            {
                'question': 'If CAT is coded as 3120, how is DOG coded?',
                'options': ['4157', '4158', '4159', '4160'],
                'correct': 0,
                'explanation': 'C=3, A=1, T=20. Similarly, D=4, O=15, G=7, so DOG = 4157'
            },
            {
                'question': 'Find the odd one out: Apple, Banana, Orange, Carrot',
                'options': ['Apple', 'Banana', 'Orange', 'Carrot'],
                'correct': 3,
                'explanation': 'Carrot is a vegetable, while others are fruits'
            },
            {
                'question': 'If RED is coded as 1854, how is BLUE coded?',
                'options': ['2122155', '2122156', '2122157', '2122158'],
                'correct': 0,
                'explanation': 'R=18, E=5, D=4. B=2, L=12, U=21, E=5, so BLUE = 2122155'
            },
            {
                'question': 'Complete: If all birds can fly, and penguins are birds, then...',
                'options': ['All penguins can fly', 'Some penguins can fly', 'Penguins cannot fly', 'This contradicts the premise'],
                'correct': 3,
                'explanation': 'This creates a logical contradiction since penguins are birds but cannot fly'
            },
            {
                'question': 'What comes next: 1, 4, 9, 16, 25, ?',
                'options': ['30', '36', '40', '45'],
                'correct': 1,
                'explanation': 'These are perfect squares: 1², 2², 3², 4², 5², so next is 6² = 36'
            },
            {
                'question': 'If today is Wednesday, what day was it 3 days ago?',
                'options': ['Sunday', 'Monday', 'Tuesday', 'Thursday'],
                'correct': 0,
                'explanation': 'Wednesday - 3 days = Sunday'
            }
        ]
        self.create_questions(category, questions_data)
    
    def create_english_grammar_questions(self, category):
        questions_data = [
            {
                'question': 'Choose the correct sentence:',
                'options': ['I have went to the store', 'I have gone to the store', 'I have go to the store', 'I have going to the store'],
                'correct': 1,
                'explanation': 'The correct past participle of "go" is "gone", not "went"'
            },
            {
                'question': 'Which sentence uses the correct subject-verb agreement?',
                'options': ['The team are playing well', 'The team is playing well', 'The team were playing well', 'The team be playing well'],
                'correct': 1,
                'explanation': '"Team" is a collective noun and takes singular verb "is"'
            },
            {
                'question': 'Choose the correct form: "Neither John nor Mary _____ present."',
                'options': ['was', 'were', 'are', 'be'],
                'correct': 0,
                'explanation': 'With "neither...nor", the verb agrees with the nearest subject (Mary - singular), so "was" is correct'
            },
            {
                'question': 'Identify the error: "She don\'t like coffee."',
                'options': ['She', "don't", 'like', 'coffee'],
                'correct': 1,
                'explanation': 'Should be "doesn\'t" because "she" is third person singular'
            },
            {
                'question': 'Choose the correct preposition: "I am good _____ mathematics."',
                'options': ['at', 'in', 'on', 'with'],
                'correct': 0,
                'explanation': 'The correct preposition with "good" when referring to a subject is "at"'
            },
            {
                'question': 'Which is the correct past tense of "lie" (to recline)?',
                'options': ['lied', 'lay', 'lain', 'laid'],
                'correct': 1,
                'explanation': 'The past tense of "lie" (to recline) is "lay"'
            },
            {
                'question': 'Choose the correct sentence:',
                'options': ['Its a beautiful day', "It's a beautiful day", 'Its\' a beautiful day', 'Its\'s a beautiful day'],
                'correct': 1,
                'explanation': '"It\'s" is the contraction of "it is"'
            },
            {
                'question': 'Which sentence is grammatically correct?',
                'options': ['Me and him went to the store', 'Him and I went to the store', 'He and I went to the store', 'I and he went to the store'],
                'correct': 2,
                'explanation': 'Subject pronouns (he, I) should be used, and "I" comes last in a compound subject'
            },
            {
                'question': 'Choose the correct form: "I _____ studying for three hours."',
                'options': ['have been', 'has been', 'am been', 'was been'],
                'correct': 0,
                'explanation': 'Present perfect continuous: "have been" + verb-ing'
            },
            {
                'question': 'Which sentence uses the correct article?',
                'options': ['An university', 'A university', 'The university', 'University'],
                'correct': 1,
                'explanation': 'Use "a" before words starting with a consonant sound, even if they start with a vowel letter'
            }
        ]
        self.create_questions(category, questions_data)
    
    def create_questions(self, category, questions_data):
        for q_data in questions_data:
            question, created = TestQuestion.objects.get_or_create(
                category=category,
                question_text=q_data['question'],
                defaults={
                    'explanation': q_data.get('explanation', ''),
                    'difficulty': 'medium'
                }
            )
            
            if created:
                # Create options
                for idx, option_text in enumerate(q_data['options']):
                    TestOption.objects.create(
                        question=question,
                        option_text=option_text,
                        is_correct=(idx == q_data['correct'])
                    )
                self.stdout.write(f'  Created question: {q_data["question"][:50]}...')


