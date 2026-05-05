from django.http import HttpResponse
from django.shortcuts import render, redirect
from mysite.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

def login(request):
    if request.user == "AnonymousUser":
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
        return redirect('/')
    
    print('Bad username or password')
    return redirect('/login')

def boardview(request):
    if request.user:
        posts = Post.objects.all()
        return render(request, 'board.html', {'posts': posts})
    else:
        return redirect('login/')

def newpost(request):
    title = request.POST.get('title')
    body = request.POST.get('body')

    admin = User.objects.first()
    p = Post(title=title, body=body, pub_date=timezone.now(), author=admin)
    p.save()
    return redirect('/')