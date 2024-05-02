import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


TYPES = (
        ('Lecture', 'Lecture'),
        ('Practice_Problems', 'Practice Problems'),
    )
class Ebook(models.Model):
    TYPES = (
        ('Lecture', 'Lecture'),
        ('Practice_Problems', 'Practice Problems'),
    )
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    year_of_publication = models.CharField(max_length=200, blank=True)
    short_description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    ebooks_type = models.CharField(max_length=50, choices=TYPES, null=True)

    def e_books_folder(self, filename):
        return os.path.join('E-books', filename)
    
    def e_books_cover(self, filename):
        return os.path.join('E-books', 'covers', filename)

    cover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=e_books_cover,
        help_text="Valid Ebook formats: jpg, png",
        validators=[
            FileExtensionValidator(["jpg", "png"])
        ],
    )

    files = models.FileField(
        null=True,
        upload_to=e_books_folder,
        help_text="Valid Ebook formats: pdf, docx",
        validators=[
            FileExtensionValidator(["pdf", "docx"])
        ],
    )

    def generate_unique_slug(self):
        return str(uuid.uuid4())[:8]

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
