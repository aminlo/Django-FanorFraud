from django.shortcuts import render
from django.http import HttpResponse

def index(request, pagename=''):
    pagename = '/' + pagename
    context = {
        'title': 'Welcome to the Quiz App'
    }
    return render(request, 'generalhome.html', context)