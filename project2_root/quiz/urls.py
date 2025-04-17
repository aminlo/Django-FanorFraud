from django.urls import path
from . import views

urlpatterns = [
    # Taking the Quiz (Function-based)
    path('get-questions/start', views.get_questions, {'is_start': True}, name='get-questions-start'),
    path('get-questions', views.get_questions, {'is_start': False}, name='get-questions'),
    path('get-answer', views.get_answer, name='get-answer'),
    path('get-finish', views.get_finish, name='get-finish'),

    # Quiz Management (Refer to week 10) (Class-based)
    path('manage/', views.QuizList.as_view(), name='quiz-manage'),
    path('series/<str:imdb_id>/quiz/create/', views.QuizCreate.as_view(), name='quiz-create'),
    path('<int:pk>/', views.QuizDetail.as_view(), name='quiz-detail'),
    path('<int:pk>/update/', views.QuizUpdate.as_view(), name='quiz-update'),
    path('<int:pk>/delete/', views.QuizDelete.as_view(), name='quiz-delete'),
    path('<int:quiz_id>/question/create/', views.QuestionCreate.as_view(), name='question-create'),
    path('question/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
]
