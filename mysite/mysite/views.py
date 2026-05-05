from django.http import HttpResponse
from django.shortcuts import render, redirect
from mysite.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

def get_username(request):
    return request.COOKIES.get('username', None)


def login(request):
    username = get_username(request)
    if username:
        print(request.user)
        return redirect('/')
    return render(request, 'login.html', {})

def loginHandle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    u = User.objects.filter(username=username).first()
    if not u:
        print('this user does not exist')
        return redirect('/login')

    if u.check_password(password):
        print('Successfully logged in')
        # Give session id
        response = redirect('/')
        response.set_cookie('username', username)
        return response
    
    print('Bad username or password')
    return redirect('/login')

def boardview(request):
    username = get_username(request)
    if username:
        posts = Post.objects.all()
        return render(request, 'board.html', {'posts': posts, 'user': username})
    else:
        return redirect('login/')

def newpost(request):
    title = request.POST.get('title')
    body = request.POST.get('body')

    admin = User.objects.first()
    p = Post(title=title, body=body, pub_date=timezone.now(), author=admin)
    p.save()
    return redirect('/')

def logout(request):
    response = redirect('/login/')
    response.delete_cookie('username')
    return response