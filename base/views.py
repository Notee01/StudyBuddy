from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import resize_image
from .models import Room, Topic, Message, User, Certificate
from survey.models import SurveyResponse
from .forms import RoomForm, UserForm

import time

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username of Password does not exist")



    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 
               'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST": 
        pic_ = None
        file_ = None
        pic = request.FILES.get('pic')  # Access uploaded file using request.FILES
        body = request.POST.get('body')
        
        if pic: 
            file_extension = pic.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png']:
                resized_img = resize_image(pic, 800, 600)

                # Save the resized image to a BytesIO object
                resized_img_io = BytesIO()
                format_ = 'JPEG'

                # Check the format of the uploaded image
                if pic.name.lower().endswith('.png'):
                    format_ = 'PNG'

                resized_img.save(resized_img_io, format=format_)
                resized_img_io.seek(0)

                # Construct filename
                filename = f"{int(time.time())}_{room.id}_{Message.objects.count() + 1}."

                # Determine the correct file extension based on the format
                if format_ == 'JPEG':
                    filename += "jpg"
                elif format_ == 'PNG':
                    filename += "png"

                # Assign the resized image to the pic variable for saving
                pic_ = InMemoryUploadedFile(resized_img_io, None, filename, f'image/{format_.lower()}', resized_img_io.tell(), None)
            else:
                file_ = pic
            
            if not body.strip() and pic:
                body = pic_ or file_

        message, created = Message.objects.get_or_create(
        user=request.user,
        room=room,
        body=body
        )
            
        if pic_ is not None:
            message.pic = pic_
            message.save()  # Save the message after adding the pic

        if file_ is not None:
            message.file = file_
            message.save()

        

        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/forum/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    certificates = user.certificates.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics,
               'certificates': certificates,}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
            
        )
        return redirect('home')
    context = {'form':form, 'topics': topics}
    return render(request, 'base/forum/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/forum/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/forum/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/forum/activity.html', {'room_messages': room_messages})


def certificate_list(request):
    certificates = Certificate.objects.filter(user=request.user)

    context = {'certificates', certificates}
    return render(request, 'base/profile.html', context)

@receiver(post_save, sender=SurveyResponse)
def create_certificate(sender, instance, created, **kwargs):
    if created:  # Check if the survey response is newly created
        user = instance.user
        title = instance.course

        Certificate.objects.get_or_create(user=user, title=title)

        print('created successfuly')