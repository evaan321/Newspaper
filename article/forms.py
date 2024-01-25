from django import forms
from .models import  *

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['photo', 'headline', 'body', 'category']