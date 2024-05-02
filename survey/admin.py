from django.contrib import admin
from .models import SurveyCategory, SurveyQuestion, SurveyResponse, SurveyResponseTally

class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 1  # Number of extra forms to display

class SurveyCatAdmin(admin.ModelAdmin):
    inlines = (SurveyQuestionInline,)

admin.site.register(SurveyCategory, SurveyCatAdmin)
admin.site.register(SurveyQuestion)

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_filter = ['course', 'question', 'user']
    list_display = ['course', 'question', 'user', 'response']

@admin.register(SurveyResponseTally)
class SurveyResponseTallyAdmin(admin.ModelAdmin):
    list_filter = ['course', 'question', 'response_count']
    list_display = ['course', 'question', 'response_count']