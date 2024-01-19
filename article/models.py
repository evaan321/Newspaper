from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    headline = models.CharField(max_length=255)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publishing_time = models.DateTimeField(auto_now_add=True)
    ratings = models.ManyToManyField(User, through='Rating')

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.IntegerField()