from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Category, Rating
from .forms import  RatingForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import send_mail,EmailMessage
from django.db.models import Avg

@login_required
def article_list(request, category_slug=None):
    articles = Article.objects.all()
    categories = Category.objects.all()
    for article in articles:
        article.average_rating = Rating.objects.filter(article=article).aggregate(Avg('value'))['value__avg']
    
        

    context = {'articles': articles,'categories':categories}
    return render(request, 'article_list.html', context)

# def article_list_by_category(request, category_name):
#     categories = Category.objects.all()
#     articles = Article.objects.filter(category__name=category_name)
#     context = {'articles': articles, 'categories': categories, 'selected_category': category_name}
#     return render(request, 'article_list.html', context)
@login_required
def article_list_by_category(request, category_name):
    categories = Category.objects.all()
    articles = Article.objects.filter(category__name=category_name)
    for article in articles:
        article.average_rating = Rating.objects.filter(article=article).aggregate(Avg('value'))['value__avg']
    
   

    
    

    context = {'articles': articles, 'categories': categories, 'selected_category': category_name}
    return render(request, 'cat_article.html', context)
@login_required
def article_detail(request,article_id):
    article = get_object_or_404(Article, id=article_id)
    rating_form = RatingForm()
  
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.article = article
            rating.save()
            subject = 'Confirm Your Email'
            message = f"Thank you for the rating "
            from_email = 'evaanrahman2@gmail.com'
            to_email = [request.user.email]
            

            send_mail(subject, message, from_email, to_email)
            
            return redirect('article_list')
            

    average_rating = Rating.objects.filter(article=article).aggregate(Avg('value'))['value__avg']

    context = {'article': article, 'rating_form': rating_form, 'average_rating': average_rating}
    return render(request, 'article_detail.html', context)

