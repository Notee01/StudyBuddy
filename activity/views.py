from .models import Activity
from django.shortcuts import render, HttpResponse, get_object_or_404
from course.models import Course, Lesson
from django.http import JsonResponse

def get_active_courses(request):
    activities = request.user.activities.filter(status=Activity.STARTED).select_related('course')
    courses = set(activity.course for activity in activities)
    return render(request, 'base/courses/courses.html', {'courses': courses})

def track_started(request, course_slug, video_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, slug=video_slug)
    activity, created = Activity.objects.get_or_create(
        created_by=request.user,
        course=course,
        lesson=lesson,
    )
    return HttpResponse({'activity': activity})

def update_activity_status(request, course_slug, video_slug):
    if request.is_ajax():
        activity = get_object_or_404(Activity, created_by=request.user, course__slug=course_slug, lesson__slug=video_slug)
        if activity.status != Activity.DONE:
            activity.status = Activity.DONE
            activity.save()
        return JsonResponse({'activity': activity})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated'}, status=400)

def progress_tracking(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lessons_count = course.lesson_set.count()
    return HttpResponse({'course': course, 'lessons_count': lessons_count})


    

 



