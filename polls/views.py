from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.models import Question, Choice
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import questionform
from django.shortcuts import redirect


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/diagramm.html'


@login_required
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request,
                      'polls/detail.html', {
                          'question': p,
                          'error_message': "You didn't select a choice.",
                      }
                      )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


@login_required
def index(request):
    p = Question
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(
        request,
        'polls/index.html',
        context={'num_visits': num_visits, 'question': p,
                 'latest_question_list': latest_question_list}
    )


def profil(request, user_id):
    users_list = User.objects.all()
    user_ID = int(user_id)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(
        request,
        'polls/profile.html',
        context={'users_list': users_list, 'user_ID': user_ID,
                 'latest_question_list': latest_question_list}
    )

def creation_quest(request):

    if request.method  == "POST":
        form = questionform(request.POST)
        if form.is_valid():
            quest = Question.create(
                question_text= form.cleaned_data['q_text'],
                pub_date = timezone.now(),
                done_by = request.user
            )
            quest.save()
            return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = questionform()
    return render(request, 'polls/question_create.html', {'form': form})