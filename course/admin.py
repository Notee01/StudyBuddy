from django.contrib import admin
from .models import Course, Category, Lesson_topic, Lesson, LessonIntroduction

admin.site.register(Course)
admin.site.register(Category)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class LessonTopicAdmin(admin.ModelAdmin):
    list_filter = ('course',)
    list_display = ('title', 'course')
    inlines = [LessonInline]

class LessonAdmin(admin.ModelAdmin):
    list_filter = ('course', 'lesson_topic')
    list_display = ('title', 'course', 'lesson_topic')

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Lesson_topic, LessonTopicAdmin)




