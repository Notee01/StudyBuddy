from django.db import models
from django.conf import settings
from course.models import Lesson_topic
import os
from random import shuffle

User = settings.AUTH_USER_MODEL

class Quiz(models.Model):
    topic = models.ForeignKey(Lesson_topic, related_name="quiz_topic", on_delete=models.CASCADE)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text='duration of quiz in minutes')
    required_score_to_pass = models.IntegerField(help_text='required score to pass the quiz')
    

    def __str__(self):
        return str(self.topic.title)
    
    def get_questions(self):
        questions = list(self.question_set.all())
        shuffle(questions)
        return questions[:self.number_of_questions]
    
    class Meta:
        verbose_name = 'Quizzes'

class Question(models.Model):
    question = models.CharField(max_length=250, blank=True)

    def image_path(self, filename):
        return os.path.join('Questions', str(self.quiz.topic), filename)
    
    image = models.ImageField(upload_to=image_path, null=True, blank=True, help_text="Add image if applicable")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    name = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.question}, answer: {self.name}, correct: {self.correct}"

REMARKS=('Pass', 'Pass'), ('Fail', 'Fail')

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="quiz", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    result = models.CharField(max_length=10, choices=REMARKS, blank=True)
    attempts = models.IntegerField(default=0)
    

    def save(self, *args, **kwargs):
        # Set the result based on the score
        self.result = 'Pass' if self.score >= self.quiz.required_score_to_pass else 'Fail'
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.quiz}')
