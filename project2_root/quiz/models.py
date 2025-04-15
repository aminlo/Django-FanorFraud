from django.db import models

class Quiz(models.Model):
  name = models.CharField(max_length=300)

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