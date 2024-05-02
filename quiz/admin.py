from django.contrib import admin
from .models import Quiz, Question, Answer, Result

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')
    inlines = [AnswerInline]


admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)




