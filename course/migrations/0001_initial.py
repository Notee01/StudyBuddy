# Generated by Django 4.2.7 on 2024-03-19 16:35

import course.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('course_code', models.CharField(max_length=200, null=True, unique=True)),
                ('crhr', models.IntegerField(default=0, null=True)),
                ('year', models.IntegerField(default=0)),
                ('semester', models.CharField(choices=[('First', 'First'), ('Second', 'Second')], max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(to='course.category')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson_topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_topic', to='course.course')),
            ],
        ),
        migrations.CreateModel(
            name='LessonIntroduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('introduction_video', models.FileField(help_text='Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3', null=True, upload_to=course.models.LessonIntroduction.introduction_video_upload_path, validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])])),
                ('lesson_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intro', to='course.lesson_topic')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('video', models.FileField(help_text='Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3', null=True, upload_to=course.models.Lesson.introduction_video_upload_path, validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])])),
                ('course', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.course')),
                ('lesson_topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_topic', to='course.lesson_topic')),
            ],
        ),
    ]
