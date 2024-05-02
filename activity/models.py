from django.conf import settings
from django.db import models
from course.models import Course, Lesson, Lesson_topic

User = settings.AUTH_USER_MODEL

class Activity(models.Model):
    STARTED = 'started'
    DONE = 'done'
    PENDING = 'pending'

    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (DONE, 'Done'),
        (PENDING, 'Pending')
    )
    course = models.ForeignKey(Course, related_name="activities", on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name="activities", on_delete=models.CASCADE)
    lesson_topic = models.ForeignKey(Lesson_topic, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STARTED)
    created_by = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)

    @property
    def lesson_topic(self):
        return self.lesson.lesson_topic if self.lesson else None

    def __str__(self):
        return f"{self.course} -- {self.lesson_topic} {self.lesson}"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.lesson.title}"
