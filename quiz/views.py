from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from course.models import Course
from activity.models import Activity
from .models import Quiz, Question, Answer, Result

def quiz_view(request, slug, topic_slug):
    course = get_object_or_404(Course, slug=slug)
    quizzes = Quiz.objects.filter(topic__course=course)
    title = course.lesson_topic.get(slug=topic_slug)
    quiz = quizzes.get(topic__slug=topic_slug)

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
    for topic in course.lesson_topic.all():
        status = all(activity.status == Activity.DONE for activity in user_activities.filter(lesson__lesson_topic=topic))
        is_previous_assessment_passed = topic.has_passed_previous_assessment(request.user)
        lesson_statuses = [(lesson, lesson.get_activity_statuses(request.user)) for lesson in topic.lesson_topic.all()]
        all_activities_done_dict.append((topic, status, is_previous_assessment_passed, lesson_statuses))

    context = {
        "course": course, 
        "title": title,
        "quiz": quiz,
        "current_status": current_status,
        "all_activities_done_dict": all_activities_done_dict,     
    }

    return render(request, "quiz/quiz.html", context)

def quiz_view_confirm(request, slug, topic_slug):
    course = get_object_or_404(Course, slug=slug)
    quiz = get_object_or_404(Quiz, topic__slug=topic_slug)
    start_quiz = course.lesson_topic.get(slug=topic_slug)

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
    for topic in course.lesson_topic.all():
        status = all(activity.status == Activity.DONE for activity in user_activities.filter(lesson__lesson_topic=topic))
        is_previous_assessment_passed = topic.has_passed_previous_assessment(request.user)
        lesson_statuses = [(lesson, lesson.get_activity_statuses(request.user)) for lesson in topic.lesson_topic.all()]
        all_activities_done_dict.append((topic, status, is_previous_assessment_passed, lesson_statuses))

    user_results = Result.objects.filter(quiz=quiz, user=request.user).order_by('-id')
    attempts = user_results.count()
    for i, result in enumerate(user_results):
        result.attempt_number = attempts - i

    context = {
        "course": course,
        "quiz": quiz,
        "start_quiz": start_quiz,
        "current_status": current_status,
        "all_activities_done_dict": all_activities_done_dict,
        "user_results": user_results,
    }
    return render(request, "quiz/quiz_confirmation.html", context)

def quiz_data_view(request, slug, topic_slug):
    course = get_object_or_404(Course, slug=slug)
    quiz = get_object_or_404(Quiz, topic__slug=topic_slug)

    questions = []
    for question in quiz.get_questions():
        answers = [answer.name for answer in question.get_answers()]
        image_url = request.build_absolute_uri(question.image.url) if question.image else None
        questions.append({
            'question': str(question),
            'answers': answers,
            'image_url': image_url,  # Include image URL in the JSON response
        })
    
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })
    

def quiz_data_submit(request, slug, topic_slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all()
    topics = course.lesson_topic.all()
    if  request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for key in data_.keys():
            print('key ', key)
            question = Question.objects.get(question=key)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(topic__slug=topic_slug)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        result = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.question)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.name:
                        if a.correct:
                            score += 1
                            correct_answer = a.name
                    else:
                        if a.correct:
                            correct_answer = a.name
                
                result.append({str(q): {'correct_answer': correct_answer, 'answer': a_selected}})
            else:
                result.append({str(q): 'no answer'})

        quiz.attempts = F('attempts') + 1
        quiz.save()
        score_ = score * multiplier

        result_ = 'Pass' if score_ >= quiz.required_score_to_pass else 'Fail'
        Result.objects.get_or_create(quiz=quiz, user=user, score=score_, result=result_)
        
        quizzes = Quiz.objects.filter(topic__course=course)
        completed_quizzes = Result.objects.filter(quiz__in=quizzes, user=request.user, result='Pass')

        all_quizzes_completed = completed_quizzes.count() == quizzes.count()

        if score_ >= quiz.required_score_to_pass:
            response_data = {'pass': True, 'score': score_, 'results': result, 'all_quizzes_completed': all_quizzes_completed}
        else:
            response_data = {'pass': False, 'score': score_, 'results': result, 'all_quizzes_completed': all_quizzes_completed}

        return JsonResponse(response_data)