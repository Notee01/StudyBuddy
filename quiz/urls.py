from django.urls import path
from . import views 

app_name = 'quizzes'

urlpatterns = [
    path("<slug:slug>/<slug:topic_slug>/", views.quiz_view, name="quiz_view"),
    path("<slug:slug>/<slug:topic_slug>/confirm-quiz/", views.quiz_view_confirm, name="quiz_view_confirm"),
    path("<slug:slug>/<slug:topic_slug>/submit/", views.quiz_data_submit, name="quiz-data-submit"),
    path("<slug:slug>/<slug:topic_slug>/data/", views.quiz_data_view, name="quiz-data-view"),

]

