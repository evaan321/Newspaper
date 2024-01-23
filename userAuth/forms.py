from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
from article.models import *


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['photo', 'headline', 'body', 'category']