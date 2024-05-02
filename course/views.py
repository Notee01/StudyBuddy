from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz, Result
from .models import Course, Lesson, LessonIntroduction
from activity.models import Activity

@login_required(login_url='login')
def coursesPage(request):
    courses = Course.objects.all()
    user_activities = Activity.objects.filter(created_by=request.user)

    course_status_info = []

    for course in courses:
        lessons_count = course.lessons.count()
        quizzes_count = Quiz.objects.filter(topic__course=course).count()
        lessons_ = course.lessons.first()

        user_activity_count = user_activities.filter(course=course, status=Activity.DONE).count()
        passed_quizzes_count = Result.objects.filter(quiz__topic__course=course, user=request.user, result='Pass').count()

        try:
            completion_percentage = round(((user_activity_count + passed_quizzes_count) / (lessons_count + quizzes_count)) * 100, 2)
        except ZeroDivisionError:
            completion_percentage = 0
        except Exception as e:
            print(f"An error occurred: {e}")
            completion_percentage = None
            
        status = 'Incomplete'
        if user_activity_count:
            if completion_percentage == 100.0:
                status = "Completed"
            elif completion_percentage > 0:
                status = "Started"

        course_info = {
            'course': course,
            'status': status,
            'lessons_count': lessons_count,
            'completion_percentage': completion_percentage,
            'first_lesson': lessons_
        }
        course_status_info.append(course_info)

    context = {'course_status_info': course_status_info}
    return render(request, 'courses.html', context)

def lessonintroPage(request, slug, video_slug):
    course = get_object_or_404(Course, slug=slug)
    topics = course.lesson_topic.all()

    try:
        vid_intro = LessonIntroduction.objects.get(slug=video_slug, lesson_topic__course=course)
    except LessonIntroduction.DoesNotExist:
        vid_intro = None

    quizzes = Quiz.objects.filter(topic__course=course)
    results = Result.objects.filter(quiz__in=quizzes, user=request.user, result='Pass') 
    try:
        current_status = round((results.count() / quizzes.count()) * 100, 2)
    except ZeroDivisionError:
        current_status = 0
    except Exception as e:
        print(f"An error occurred: {e}")
        current_status = None

    user_activities = Activity.objects.filter(created_by=request.user, course=course)
    all_activities_done_dict = []

    for topic in topics:
        status = all(activity.status == Activity.DONE for activity in user_activities.filter(lesson__lesson_topic=topic))
        is_previous_assessment_passed = topic.has_passed_previous_assessment(request.user)
        lesson_statuses = [(lesson, lesson.get_activity_statuses(request.user)) for lesson in topic.lesson_topic.all()]
        all_activities_done_dict.append((topic, status, is_previous_assessment_passed, lesson_statuses))

    context = {
        "course": course,
        "topics": topics,
        "current_status": current_status,
        "vid_intro": vid_intro,
        "all_activities_done_dict": all_activities_done_dict,
    }
    
    return render(request, 'lesson_video_intro.html', context)

def videoPage(request, video_slug, slug):
    course = get_object_or_404(Course, slug=slug)
    vid_lesson = get_object_or_404(Lesson, slug=video_slug)

    # Create an activity for the current lesson if it doesn't exist
    if not Activity.objects.filter(course=course, created_by=request.user, lesson=vid_lesson).exists():
        Activity.objects.create(course=course, created_by=request.user, lesson=vid_lesson)

    quizzes = Quiz.objects.filter(topic__course=course)
    results = Result.objects.filter(quiz__in=quizzes, user=request.user, result='Pass') 
    try:
        current_status = round((results.count() / quizzes.count()) * 100, 2)
    except ZeroDivisionError:
        current_status = 0
    except Exception as e:
        print(f"An error occurred: {e}")
        current_status = None
        
    user_activities = Activity.objects.filter(created_by=request.user, course=course)
    topics = course.lesson_topic.all()
    all_activities_done_dict = []

    for topic in topics:
        status = all(activity.status == Activity.DONE for activity in user_activities.filter(lesson__lesson_topic=topic))
        is_previous_assessment_passed = topic.has_passed_previous_assessment(request.user)
        lesson_statuses = [(lesson, lesson.get_activity_statuses(request.user)) for lesson in topic.lesson_topic.all()]
        all_activities_done_dict.append((topic, status, is_previous_assessment_passed, lesson_statuses))

    context = {
        "vid_lesson": vid_lesson, 
        "course": course, 
        "current_status": current_status,
        "all_activities_done_dict": all_activities_done_dict,
    }
    return render(request, 'lesson_video.html', context)

    




