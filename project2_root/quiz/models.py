from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

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

class QuizResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username}'s result for {self.quiz.name} - {self.percentage}%"