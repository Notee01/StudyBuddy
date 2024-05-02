from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),

    #COURSE PAGE
    path('courses/', include('course.urls', namespace='course')),

    #ACTIVITY PAGE
    path('', include('activity.urls')),

    #QUIZ PAGE
    path('quiz/', include('quiz.urls', namespace='quizzes')),

    #MATERIAL PAGE
    path('material/', include('material.urls', namespace='material')),
    
    #SURVEY PAGE
    path('feedback/', include('survey.urls', namespace='survey')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)