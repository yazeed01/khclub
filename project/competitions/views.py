from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Questions, Answers, CorrectAnswer, Quiz, Points
from django.contrib import messages
from django.views.generic import ListView
from .forms import CorrectAnswerForm


# Create your views here.

class CompetitionView(ListView):
    queryset = Quiz.objects.filter(display=True).order_by("-created_at")
    paginate_by = 9
    context_object_name = "comps"
    template_name = 'competitions.html'



#TODO: Edit the rest.

def quiz(request, slug=None):
    try:
        ques= get_object_or_404(Questions, quiz__slug=slug)
        quiz_slug = Quiz.objects.get(slug=slug)
    except:
        messages.info(request, 'لا يوجد سؤال')
        return redirect('competitions:competition')

    if request.user.is_authenticated:

        try:
            ans = CorrectAnswer.objects.get(correct_answer__question__quiz__slug=slug, created_by=request.user)
            if ans:
                ans = False
                messages.info(request, 'لقد حللت هذا السؤال من قبل.')
                return HttpResponseRedirect('/competitions/')
                # return redirect('competitions:competition')
        except:
            ans = True

    
        if request.method == "POST":
            if request.POST.get('flexRadioDefault'):
                an = Answers.objects.get(id=request.POST.get('flexRadioDefault'))
                form = CorrectAnswerForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.correct_answer = an
                    post.created_by = request.user
                    post.save()

                    if an.is_correct == True:
                        points, created = Points.objects.get_or_create(correct_answer_point__created_by=request.user,correct_answer_point=post,proints=5)
                    else:
                        pass
                    
                    messages.success(request, 'شكراً لك على المشاركة، تم إرسال إجابتك.')
                    return redirect('competitions:competition')
                else:
                    form = CorrectAnswerForm()
            else:
                messages.error(request, 'هذا الحق مطلوب')
                an = None
        
    else:
        return redirect('main:home')
    
    context = {'ques':ques,'ans':ans}

    return render(request, 'quiz.html', context)


class AdConManaView(ListView):
    model = Quiz
    context_object_name = "quizs"
    template_name = 'con_manage/ad_con_mana.html'
    paginate_by = 9


def ad_con_mana_quiz(request,qu_adm_id):
    if request.user.is_superuser:
        try:
            que = get_object_or_404(Questions, quiz_id=qu_adm_id)
        except:
            quiz = Quiz.objects.get(id=qu_adm_id)
            messages.info(request, f'لا يوجد سؤال في ( {quiz} ) ضع سؤال ثم حاول مجدداً')
            return redirect('competitions:ad_con_mana')
        coAns = CorrectAnswer.objects.select_related('correct_answer__question__quiz').filter(correct_answer__question__quiz=qu_adm_id)
        
        if show := request.GET.get("show"):
            if show == "True" or show == "False":
                coAns = CorrectAnswer.objects.select_related('correct_answer__question__quiz').filter(correct_answer__question__quiz=qu_adm_id, correct_answer__is_correct=show)
            else:
                coAns
        else:
            # Get All for show in Table.
            coAns
        
        # Get just for correct answer 'True'
        coAns_true = CorrectAnswer.objects.filter(correct_answer__question__quiz=qu_adm_id, correct_answer__is_correct=True)
        
        
        cou_conAns = CorrectAnswer.objects.select_related('correct_answer__question__quiz').filter(correct_answer__question__quiz=qu_adm_id)
        cou_conAns_All = cou_conAns.count()
        cou_conAns_True = cou_conAns.filter(correct_answer__is_correct=True).count()
        cou_conAns_False = cou_conAns.filter(correct_answer__is_correct=False).count()
        
        
        import random
        if coAns_true:
            random_coAns = random.choice(coAns_true)
        else:
            random_coAns = None
        context = {
            'coAns':coAns,
            'que':que,
            'random_coAns':random_coAns,
            'qu_adm_id':qu_adm_id,
            'cou_conAns_False':cou_conAns_False,
            'cou_conAns_True':cou_conAns_True,
            'cou_conAns_All':cou_conAns_All,
        }
        return render(request, 'con_manage/ad_con_mana_quiz.html', context)
    else:
        return render(request, 'erorrs/404.html', status=404)