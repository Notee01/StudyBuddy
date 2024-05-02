from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from course.models import Course
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import Counter
from .models import SurveyQuestion, SurveyResponse, SurveyCategory, SurveyResponseTally
import re
import json
# Create your views here.

def surveyPage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    survey_categories = SurveyCategory.objects.filter(survey=course)
    all_questions = SurveyQuestion.objects.filter(category__in=survey_categories)

    questions_per_page = 5

    paginator = Paginator(all_questions, questions_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'survey_questions': page_obj,
        'course': course
    }

    return render(request, 'base.html', context)

def submit_survey(request, slug):
    if request.method == 'POST' and request.is_ajax():
        course = get_object_or_404(Course, slug=slug)
        question_responses = request.POST.dict()  
        question_responses.pop('csrfmiddlewaretoken', None)  

        survey_responses = []
        for question_id, response in question_responses.items():
            survey_response, created = SurveyResponse.objects.get_or_create(
                course=course, 
                question_id=question_id, 
                user=request.user,
                defaults={'response': response}  
            )
            

        return JsonResponse({'message': 'Survey responses saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@receiver(post_save, sender=SurveyResponse)
def update_survey_response_tally(sender, instance, **kwargs):
    course_id = instance.course_id
    question_id = instance.question_id
    
    responses = SurveyResponse.objects.filter(course_id=course_id, question_id=question_id)
    likert_responses = [response.response for response in responses if response.response in ['SD', 'D', 'N', 'A', 'SA']]
    response_count = Counter(likert_responses)
    response_count_json = json.dumps(response_count)
    
    tally, created = SurveyResponseTally.objects.get_or_create(course_id=course_id, question_id=question_id)
    tally.response_count = response_count_json 
    tally.save()