from django.urls import path
from . import views 

urlpatterns = [
    path('get_active_courses/', views.get_active_courses, name="active"),
    path('<slug:course_slug>/<slug:video_slug>/track-started', views.track_started),
    path('<slug:course_slug>/<slug:video_slug>/progress-started', views.progress_tracking),
    path('courses/<slug:course_slug>/<slug:video_slug>/lecture/update-activity-status', views.update_activity_status, name="update-activity-status")

]
