from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views.generic import TemplateView
from quiz.models import Quiz
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Quiz.objects.all().annotate(questions_count=Count('question'))
        return context

class SearchResultsView(TemplateView):
    template_name = 'searchres.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q') # gets q from form
        results = []
        if query:
            url = 'http://www.omdbapi.com/'
            params = {
                'apikey': '96881c4f',
                's': query,
                'type': 'series',
            }
            response = requests.get(url, params=params) # sends request get to omdbapi (our api)
            data = response.json()

            if data.get('Response') == 'True':
                results = data.get('Search', []) # parses data

        context['results'] = results
        return context
    
class SeriesDetailView(TemplateView):
    template_name = 'series_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imdb_id = kwargs.get('imdb_id')
        
        if imdb_id:
            response = requests.get('http://www.omdbapi.com/', params={
                'apikey': '96881c4f',
                'i': imdb_id
            })
            data = response.json()
            if data.get('Response') == 'True':
                context['series'] = data
                context['imdb_id'] = imdb_id
                context['quizzes'] = Quiz.objects.filter(imdb_id=imdb_id)
                context['can_create'] = self.request.user.is_authenticated

        return context
