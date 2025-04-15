from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('series/<str:imdb_id>/', views.SeriesDetailView.as_view(), name='series_detail'),
    path('', views.HomeView.as_view(), name='index'),

]