from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     name = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)