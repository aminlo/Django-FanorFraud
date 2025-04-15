from django.shortcuts import render
from django.http import HttpResponse

def index(request, pagename=''):
    pagename = '/' + pagename
    context = {
    }
    return render(request, 'base.html', context)