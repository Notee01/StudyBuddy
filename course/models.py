from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.dispatch import receiver
from django.apps import apps
import os
import random
import string

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generate slug automatically only if it's not set or if the title has changed
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Course(models.Model):
    FIRST = "First"
    SECOND = "Second"
    SEMESTER_CHOICES = (
        (FIRST, "First"),
        (SECOND, "Second"),
    )

    categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    title = models.CharField(max_length=200, null=True)
    course_code = models.CharField(max_length=200, unique=True, null=True)
    crhr = models.IntegerField(null=True, default=0)
    year = models.IntegerField(default=0)
    semester = models.CharField(choices=SEMESTER_CHOICES, max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate slug automatically only if it's not set or if the title has changed
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course:lesson", kwargs={"slug": self.slug})

    
class Lesson_topic(models.Model):
    course = models.ForeignKey(Course, related_name='lesson_topic', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate slug automatically only if it's not set or if the title has changed
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("quizzes:quiz_view", kwargs={"topic_slug": self.slug, "slug": self.course.slug,})
    
    def get_absolute_url_confirmed(self):
        return reverse("quizzes:quiz_view_confirm", kwargs={"topic_slug": self.slug, "slug": self.course.slug,})
    
    def get_absolute_url_intro(self):
        # Retrieve the LessonIntroduction object associated with this Lesson_topic
        intro = self.intro.first()  # Assuming there's only one introduction associated with the topic
        if intro:
            return reverse("course:lesson_intro", kwargs={"video_slug": intro.slug, "slug": self.course.slug})
        return None  
    
    def has_passed_previous_assessment(self, user):
        Result = apps.get_model('quiz', 'Result')
        previous_topics = self.course.lesson_topic.filter(id__lt=self.id)
        if not previous_topics.exists():
            return True# No previous topic, so consider it as passed
        else:
            for topic in previous_topics:
                quizzes = topic.quiz_topic.all()
                for quiz in quizzes:
                    results = Result.objects.filter(quiz=quiz, user=user)
                    if not results.exists() or results.latest('id').result != 'Pass':
                        return False
            return True
        
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, blank=True, null=True, editable=False)
    lesson_topic = models.ForeignKey(Lesson_topic, related_name='lesson_topic', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def get_activity_statuses(self, user):
        # Retrieve activities associated with the lesson for the specified user
        activities = self.activities.filter(created_by=user)
    
        # Retrieve status for each activity
        statuses = [activity.status for activity in activities]
    
        return statuses
    
    def introduction_video_upload_path(self, filename):
        return os.path.join('course_videos', str(self.lesson_topic), 'lesson', filename)

    video = models.FileField(
        null=True,
        upload_to=introduction_video_upload_path,
        help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
    )

    def generate_unique_slug(self):
        """Generate a random 5-digit slug and ensure its uniqueness."""
        while True:
            # Generate a random 5-digit number
            random_slug = ''.join(random.choices(string.digits, k=5))
            # Check if the generated slug is unique
            if not Lesson.objects.filter(slug=random_slug).exists():
                return random_slug

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = self.generate_unique_slug()

        # Set the course if lesson_topic is provided and course is not set
        if self.lesson_topic and not self.course:
            self.course = self.lesson_topic.course

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("course:lesson_video", kwargs={"video_slug": self.slug, "slug": self.course.slug,})
  

@receiver(models.signals.post_delete, sender=Lesson)
def auto_delete_files_on_delete(sender, instance, **kwargs): 
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path) 


class LessonIntroduction(models.Model):
    lesson_topic = models.ForeignKey(Lesson_topic, related_name='intro', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def introduction_video_upload_path(self, filename):
        return os.path.join('course_videos', str(self.lesson_topic), 'introduction', filename)
    
    introduction_video = models.FileField(
        null=True,
        upload_to=introduction_video_upload_path,
        help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
    )

    def save(self, *args, **kwargs):
        # Generate slug automatically only if it's not set or if the title has changed
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse("course:lesson", kwargs={"intro_slug": self.slug, "slug": self.lesson_topic.slug,})
    
    
@receiver(models.signals.post_delete, sender=LessonIntroduction)
def auto_delete_files_on_delete(sender, instance, **kwargs):
    """
    Deletes associated files from the filesystem when corresponding `Lesson` or `LessonIntroduction` objects are deleted.
    """
    if instance.introduction_video:
        if os.path.isfile(instance.introduction_video.path):
            os.remove(instance.introduction_video.path)


