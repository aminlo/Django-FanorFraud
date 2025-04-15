from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import redirect
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
    success_url = reverse_lazy('profile')  # Redirect after successful signup

    def form_valid(self, form):
        user = form.save()
        user.save()  # Save the user with the new fields (bio)
        login(self.request, self.object)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')  # Capture user_id from URL (optional)

        # If the user_id is not passed, we default to the current user's profile
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
        else:
            user = self.request.user  # Current logged-in user

        # Pass the profile data to the template
        context['profile_user'] = user
        context['is_own_profile'] = (user == self.request.user)  # Check if viewing own profile
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['bio', 'profile_picture']
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')  # Redirect after successful update

    def get_object(self, queryset=None):
        return self.request.user  # Only allow the logged-in user to edit their own profile