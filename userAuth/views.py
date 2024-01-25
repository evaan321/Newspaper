from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView
from .models import *
from .forms import *
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMessage
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings



class CustomRegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        
        token = default_token_generator.make_token(self.object)
        activation_url = f"http://127.0.0.1:8000/activate/{self.object.id}/{token}"

        subject = 'Confirm Your Email'
        message = f"Click the following link to activate your account: {activation_url}"
        from_email = 'evaanrahman2@gmail.com'
        to_email = [form.cleaned_data['email']]

        send_mail(subject, message, from_email, to_email)

        messages.success(self.request, 'Please check your email to confirm registration.')
        return response
    
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    def get_success_url(self) -> str:
        return reverse_lazy('article_list')

def home(request):
    return render(request,'home.html')


@login_required
def profile(request):
    user_model = request.user

    
    is_staff = request.user.is_staff

    
    if is_staff:
        
        
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                new_article = form.save(commit=False)
                new_article.author = user_model
                new_article.save()
                return redirect('profile')
        else:
            form = ArticleForm()

    else:
        user_articles = None
        form = None

    return render(request, 'profile.html', {'user_model': user_model, 'is_staff': is_staff, 'form': form})

@login_required
def logoutNew(request):
    logout(request)
    return redirect('article_list')

def activate(request, user_id, token):
    user = User.objects.get(pk=user_id)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('login')
    
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})

class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User  
    form_class = UserProfileForm  
    template_name = 'update_profile.html'
    success_url = reverse_lazy('profile') 
    success_message = 'Your profile has been updated successfully.'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating your profile.')
        return super().form_invalid(form)
    
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            subject = 'Contact Us Form Submission'
            message = f'Name: {name}\nEmail: {email}\n\n\n{message}'
            from_email = 'evaanrahman2@gmail.com'
            to_email = [form.cleaned_data['email']]
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            
            return redirect('article_list')
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})

def about(request):
    return render(request , 'about_us.html')