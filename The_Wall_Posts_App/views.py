from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from .models import *
from django.contrib import messages

def index(request):
    context = {
    "time": strftime("%b %d, %Y  %H:%M %p", gmtime())
    }
    return render(request, "index.html", context)
   

def register(request):
    if request.method == "GET":
        return redirect("/")
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        # messages.success(request, "You have successfully registered!")
        return redirect('/wall')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    #messages.success(request, "You have successfully logged in!")
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)


def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_messages': Message.objects.all().order_by('-created_at'),
        
    }
    return render(request, 'wall.html', context)


def post_message(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        Message.objects.create(
            message=request.POST['message'],
            user = User.objects.get(id=request.session['user_id'])
        )
    return redirect('/wall')


def post_comment(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    #create
    user = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], user=user, message=message)
    return redirect('/wall')



def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    liked_message = Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/wall')

def delete_Mesg(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    destroyed = Message.objects.get(id=id)
    print("session user id: " + str(request.session['user_id']))
    print("Message user id: " + str(destroyed.user.id))
    if ((request.session['user_id']) == destroyed.user.id):
        destroyed.delete()
    return redirect('/wall')

def delete_comment(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    destroyed = Comment.objects.get(id=id)
    print("session user id: " + str(request.session['user_id']))
    print("Message user id: " + str(destroyed.user.id))
    if ((request.session['user_id']) == destroyed.user.id):
        destroyed.delete()
    return redirect('/wall')

def edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['fname']
    edit_user.last_name = request.POST['lname']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/wall')


