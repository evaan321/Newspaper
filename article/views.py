from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Category, Rating
from .forms import  RatingForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import send_mail,EmailMessage
def article_list(request, category_slug=None):
    articles = Article.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)

    context = {'articles': articles}
    return render(request, 'article_list.html', context)

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
            

    context = {'article': article, 'rating_form': rating_form,}
    return render(request, 'article_detail.html', context)

