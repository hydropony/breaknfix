from django.http import HttpResponse
from django.shortcuts import render, redirect
from mysite.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import sqlite3

def get_username(request):
    return request.user # fix auth
    # return request.COOKIES.get('username', None)

def login(request):
    username = get_username(request)
    if username:
        print(request.user)
        return redirect('/')
    return render(request, 'login.html', {})

# def loginHandle(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
    
#     u = User.objects.filter(username=username).first()
#     if not u:
#         print('this user does not exist')
#         return redirect('/login')

#     if u.check_password(password):
#         print('Successfully logged in')
#         # Give session id
#         response = redirect('/')
#         response.set_cookie('username', username)
#         return response
    
#     print('Bad username or password')
#     return redirect('/login')

# Fix auth
def loginHandle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        response = redirect('/')
        return response
    
    return redirect('/login')

@login_required # auth fix
def boardview(request):
    username = get_username(request)
    user = User.objects.filter(username=username).first()
    myposts = Post.objects.filter(author=user)
    post_ids = [post.id for post in myposts]
    if username:
        posts = Post.objects.all()
        return render(request, 'board.html', {'posts': posts, 'user': username, 'myposts': post_ids})
    else:
        return redirect('login/')

@login_required # auth fix
def newpost(request):
    title = request.POST.get('title')
    body = request.POST.get('body')
    username = get_username(request)
    user = User.objects.filter(username=username).first()

    # Vulnerable section
    cx = sqlite3.connect('mysite/db.sqlite3')
    cu = cx.cursor()
    sql = f"""INSERT INTO mysite_post (title, body, pub_date, author_id) VALUES ('{title}', '{body}', '{timezone.now()}', {user.id});"""
    cu.execute(sql)
    cx.commit()
    cx.close()
    # End vulnerable section

    # Fix SQL injection vulnerability
    # p = Post(title=title, body=body, pub_date=timezone.now(), author=user)
    # p.save()
    # End fix
    return redirect('/')

# CSRF fix
# def delete(request):
#     id = request.POST.get('id')
#     p = Post.objects.filter(id=id)
#     p.delete()
#     return redirect('/')

@login_required # auth fix
def delete(request, id):
    p = Post.objects.filter(id=id)
    p.delete()
    return redirect('/')

# def handleLogout(request):
#     response = redirect('/login/')
#     response.delete_cookie('username') 
#     return response

# auth fix
@login_required
def handleLogout(request):
    logout(request)
    return redirect('login/')