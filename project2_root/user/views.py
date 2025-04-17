from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

def index(request, pagename=''):
    pagename = '/' + pagename
    context = {
    }
    return render(request, 'base.html', context)


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('profile')  # overrides LOGIN_REDIRECT_URL

    def get_success_url(self):
        return self.success_url

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')  # Or login page or wherever


class HomeView(View):
    def get(self, request, pagename=''):
        context = {
        }
        return render(request, 'accounts/home.html', context)
    
from .forms import CustomUserCreationForm
from .models import CustomUser



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  # Redirect after successful signup

    def form_valid(self, form):
        self.object = form.save() 
        login(self.request, self.object)  
        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get user_id or username from the URL kwargs (parsed)
        user_id = self.kwargs.get('user_id')
        username = self.kwargs.get('username')

        # If a username is provided, fetch user by username
        if username:
            user = get_object_or_404(CustomUser, username=username)
        elif user_id:  # If user_id is provided, fetch user by user_id
            user = get_object_or_404(CustomUser, pk=user_id)
        else:
            user = self.request.user  # Default to the logged-in user's profile

        
        # Add user data to the context (to be accessed as)
        context['profile_user'] = user
        context['is_own_profile'] = (user == self.request.user)  # Check if viewing own profile (flag)

        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = CustomUser
    fields = ['bio', 'profile_picture']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')  # Redirect after successful update

    def get_object(self, queryset=None):
        return self.request.user  # Only allow the logged-in user to edit their own profile