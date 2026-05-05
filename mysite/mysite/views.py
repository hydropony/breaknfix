from django.http import HttpResponse
from django.shortcuts import render, redirect
from mysite.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

def home(request):
    return HttpResponse("Hello, World!")

def boardview(request):
    posts = Post.objects.all()
    return render(request, 'board.html', {'posts': posts})

def newpost(request):
    title = request.POST.get('title')
    body = request.POST.get('body')

    admin = User.objects.first()
    p = Post(title=title, body=body, pub_date=timezone.now(), author=admin)
    p.save()
    return redirect('/')