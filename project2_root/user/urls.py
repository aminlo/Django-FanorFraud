from django.urls import path
from . import views

urlpatterns = [
    path('profile_update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_other'),  # For viewing another user's profile
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile_other_username'),
    path('home/', views.HomeView.as_view(), name='home'),   
]