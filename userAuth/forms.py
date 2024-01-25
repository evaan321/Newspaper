from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
from article.models import *
from django.contrib.auth.forms import UserChangeForm
from crispy_forms.helper import FormHelper


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['photo', 'headline', 'body', 'category']


class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] 

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.label_class = ''
        



class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)
