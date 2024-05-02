from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('<slug:slug>/', views.surveyPage, name="surveyPage"),
    path('<slug:slug>/submit', views.submit_survey, name="submit_survey"),


]