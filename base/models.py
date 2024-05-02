from django.db import models
from authUser.models import User
from django.core.validators import FileExtensionValidator
import os
from datetime import date
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    host =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()

    def image_path(self, filename):
        today_date = date.today().strftime('%Y-%m-%d')
        return os.path.join('room_images', today_date, filename)
    
    pic = models.FileField(
        upload_to=image_path, 
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(["png", "jpg", "jpeg"])
        ],)
    
    file = models.FileField(
        upload_to=image_path, 
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(["docx", "doc"])
        ],)
    
    def file_name(self):
        return os.path.basename(self.file.name) if self.file else None
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='certificates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Certificate for {self.user} in {self.title}')


    
    