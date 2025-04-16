from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from .models import Quiz, Question, Answer, QuizResult
from django.core.paginator import Paginator
from typing import Optional
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import QuizForm, QuestionForm, AnswerForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone

# Quiz Management Views (refer to week 10) (Class-based)
class QuizList(ListView):
    model = Quiz
    template_name = 'quiz/manage.html'
    context_object_name = 'quizzes'

class QuizCreate(CreateView):
    model = Quiz
    template_name = 'quiz/create.html'
    fields = ['name']
    success_url = reverse_lazy('quiz-manage')

class QuizDetail(DetailView):
    model = Quiz
    template_name = 'quiz/detail.html'

class QuizUpdate(UpdateView):
    model = Quiz
    template_name = 'quiz/update.html'
    fields = ['name']
    success_url = reverse_lazy('quiz-manage')

class QuizDelete(DeleteView):
    model = Quiz
    template_name = 'quiz/delete.html'
    success_url = reverse_lazy('quiz-manage')

# Question Management Views (Class-based)
class QuestionCreate(CreateView):
    model = Question
    template_name = 'quiz/question_create.html'
    fields = ['text']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_id'] = self.kwargs['quiz_id']
        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=4)
        context['answer_formset'] = AnswerFormSet(queryset=Answer.objects.none())
        return context
    
    def form_valid(self, form):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_id'])
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()

        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=4)
        answer_formset = AnswerFormSet(self.request.POST, queryset=Answer.objects.none())
        
        if answer_formset.is_valid():
            for form in answer_formset:
                if form.cleaned_data:
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quiz-detail', kwargs={'pk': self.kwargs['quiz_id']})

class QuestionUpdate(UpdateView):
    model = Question
    template_name = 'quiz/question_update.html'
    fields = ['text']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)
        context['answer_formset'] = AnswerFormSet(
            self.request.POST or None,
            queryset=Answer.objects.filter(question=self.object)
        )
        return context
    
    def form_valid(self, form):
        question = form.save()
        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0)
        answer_formset = AnswerFormSet(
            self.request.POST,
            queryset=Answer.objects.filter(question=question)
        )
        
        if answer_formset.is_valid():
            answer_formset.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quiz-detail', kwargs={'pk': self.object.quiz.id})

class QuestionDelete(DeleteView):
    model = Question
    template_name = 'quiz/question_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('quiz-detail', kwargs={'pk': self.object.quiz.id})



# Quiz Taking Views (Function-based) (referenced from youtube)
def start_quiz_view(request) -> HttpResponse:
    topics = Quiz.objects.all().annotate(questions_count=Count('question'))
    return render(
        request, 'start.html', context={'topics': topics}
    )

def get_questions(request, is_start=False) -> HttpResponse:
    if is_start:
        request = _reset_quiz(request)
        question = _get_first_question(request)
    else:
        question = _get_subsequent_question(request)
        if question is None:
            return get_finish(request)

    answers = Answer.objects.filter(question=question)
    request.session['question_id'] = question.id

    return render(request, 'partials/question.html', context={
        'question': question, 'answers': answers
    })

def _get_first_question(request) -> Question:
    quiz_id = request.POST.get('quiz_id')
    if not quiz_id:
        raise ValueError("No quiz_id provided")
    return Question.objects.filter(quiz_id=quiz_id).order_by('id').first()

def _get_subsequent_question(request) -> Optional[Question]:
    quiz_id = request.POST.get('quiz_id')
    if not quiz_id:
        raise ValueError("No quiz_id provided")
    
    previous_question_id = request.session.get('question_id')
    if not previous_question_id:
        raise ValueError("No previous question_id in session")

    try:
        return Question.objects.filter(
            quiz_id=quiz_id, id__gt=previous_question_id
        ).order_by('id').first()
    except Question.DoesNotExist:
        return None

def get_answer(request) -> HttpResponse:
    submitted_answer_id = request.POST.get('answer_id')
    if not submitted_answer_id:
        raise ValueError("No answer_id provided")
        
    submitted_answer = Answer.objects.get(id=submitted_answer_id)

    if submitted_answer.is_correct:
        correct_answer = submitted_answer
        request.session['score'] = request.session.get('score', 0) + 1
    else:
        correct_answer = Answer.objects.get(
            question_id=submitted_answer.question_id, is_correct=True
        )

    return render(
        request, 'partials/answer.html', context={
            'submitted_answer': submitted_answer,
            'answer': correct_answer,
        }
    )

def get_finish(request) -> HttpResponse:
    quiz = Question.objects.get(id=request.session['question_id']).quiz
    questions_count = Question.objects.filter(quiz=quiz).count()
    score = request.session.get('score', 0)
    percent = int(score / questions_count * 100)
    
    # Save the quiz result if user is authenticated
    if request.user.is_authenticated:
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=questions_count,
            percentage=percent
        )
    
    request = _reset_quiz(request)

    return render(request, 'partials/finish.html', context={
        'questions_count': questions_count, 'score': score, 'percent_score': percent
    })

def _reset_quiz(request) -> HttpRequest:
    if 'question_id' in request.session:
        del request.session['question_id']
    if 'score' in request.session:
        del request.session['score']
    return request