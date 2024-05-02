# In models.py within the 'courses' app or any suitable app
from django.db import models
from django.conf import settings
from course.models import Course

User = settings.AUTH_USER_MODEL

class SurveyCategory(models.Model):
    survey = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.survey.title

class SurveyQuestion(models.Model):
    QUESTION_TYPES = (
        ('Likert', 'Likert Scale'),
        ('OpenEnded', 'Open-Ended'),
    )

    QUESTION_CHOICES = (
        ('VP', 'Very Poor'),
        ('P', 'Poor'),
        ('F', 'Fair'),
        ('G', 'Good'),
        ('E', 'Excellent'),
    )
    category = models.ForeignKey(SurveyCategory, on_delete=models.CASCADE, null=True)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    question_text = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.question_text[:50]}..."
    

class SurveyResponse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Assuming each response is tied to a user
    response = models.CharField(max_length=100, null=True)
    
    
    def __str__(self):
        return f"Result for Question {self.question.question_text}"
    
class SurveyResponseTally(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    response_count = models.TextField()

    def __str__(self):
        return f"Tally for '{self.question}' in '{self.course}'"
    