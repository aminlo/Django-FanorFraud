from django.shortcuts import render
from django.http import HttpResponse

def quiz(request):
    return HttpResponse("Quiz Test Site")