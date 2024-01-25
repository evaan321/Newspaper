from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Category, Rating
from .forms import  RatingForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import send_mail,EmailMessage
from django.db.models import Avg
from userAuth.forms import *
from .forms import *
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView,UpdateView



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
    is_staff = request.user.is_staff
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

    context = {'article': article, 'rating_form': rating_form, 'average_rating': average_rating,'is_staff':is_staff}
    return render(request, 'article_detail.html', context)

@login_required
def addArticle(request):
    

    
    is_staff = request.user.is_staff

    
    if is_staff:
        
        
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                new_article = form.save(commit=False)
                
                new_article.save()
                return redirect('profile')
        else:
            form = ArticleForm()

    else:
        user_articles = None
        form = None

    return render(request, 'new_article.html', { 'is_staff': is_staff, 'form': form})



def generate_pdf(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    template_path = 'article_pdf_template.html'
    context = {'article': article}
    
    # Create a Django response object with appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{article.headline}.pdf"'

    # Create a PDF object using the HTML template and context data
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF from HTML using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response

class EditArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'edit_article.html'
    success_url = '/article_list/'  
    def get(self, request, *args, **kwargs):
        article = self.get_object()
     
        if request.user.is_staff or request.user == article.author:
            return super().get(request, *args, **kwargs)
    
        return render(request, 'unauthorized.html')
    
class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'delete_article.html'
    success_url = '/article_list/'  

    def get(self, request, *args, **kwargs):
        article = self.get_object()
     
        if request.user.is_staff or request.user == article.author:
            return super().get(request, *args, **kwargs)
        
        return render(request, 'unauthorized.html')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Article deleted successfully.')
        return super().delete(request, *args, **kwargs)