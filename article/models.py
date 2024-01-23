from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name

class Article(models.Model):
    photo = models.ImageField('uploads' , blank=True)
    headline = models.CharField(max_length=255)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publishing_time = models.DateTimeField(auto_now_add=True)
    ratings = models.ManyToManyField(User, through='Rating')
    def __str__(self) -> str:
        return self.headline
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])

    def __str__(self) -> str:
        return self.article.headline