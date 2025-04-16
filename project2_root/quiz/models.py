from django.db import models
from user.models import CustomUser

class Quiz(models.Model):
    name = models.CharField(max_length=300)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    imdb_id = models.CharField(max_length=20, null=True, blank=True)

class Question(models.Model):
  MULTIPLE_CHOICE = 'MC'
  QUESTION_TYPES = [
    (MULTIPLE_CHOICE, 'Multiple Choice'),
  ]
  
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default=MULTIPLE_CHOICE)

  class Meta:
    ordering = ['id']

class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  is_correct = models.BooleanField(default=False)