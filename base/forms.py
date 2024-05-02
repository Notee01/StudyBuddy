from django.forms import ModelForm
from django import forms
from .models import Room, Message
from authUser.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email']
