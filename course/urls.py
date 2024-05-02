from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.coursesPage, name="courses"),
    path('<slug:slug>/<slug:video_slug>/introduction', views.lessonintroPage, name="lesson_intro"),
    path('<slug:slug>/<slug:video_slug>/lecture', views.videoPage, name="lesson_video"),

]