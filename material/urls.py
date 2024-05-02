from django.urls import path
from . import views

app_name = 'material'

urlpatterns = [
    path('', views.ebook_list, name="materials"),
]