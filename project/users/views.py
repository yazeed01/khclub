import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

from competitions.models import CorrectAnswer, Points
from .forms import LoginForm, SignUpForm, SettingsForm
from .models import *



from django.contrib.auth import get_user_model
User = get_user_model()


class SettingView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SettingsForm
    template_name = "account.html"
    success_url = '/account'
    
    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث الملف الشخصي .')
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coAns = CorrectAnswer.objects.filter(created_by=self.request.user)
        po = Points.objects.filter(correct_answer_point__correct_answer__is_correct=True,
                                    correct_answer_point__created_by=self.request.user,
                                    )

        if sum([i.proints for i in po]):
            to_po = sum([i.proints for i in po])
        else:
            to_po = 0

        context['coAns'] = coAns
        context['to_po'] = to_po
        return context


class PasswordChange(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        messages.success(self.request, 'تم تغيير كلمة السر الخاصة بك.')
        return super().form_valid(form)


# class RegisterView(CreateView):
#     model = User
#     form_class = SignUpForm
#     template_name = "profile/signup.html"

    # def form_valid(self, form):
    #     valid = super().form_valid(form)
    #     login(self.request, self.object)
    #     return valid


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')

    return render(request, 'profile/signup.html',{'form':form})


class TeamWorkView(ListView):
    queryset = Personnel.objects.filter(display=True).order_by("order")
    context_object_name = "teams"
    template_name = "profile/team-work.html"


class PartnersView(ListView):
    queryset = Partners.objects.filter(display=True)
    context_object_name = "partners"
    template_name = "success-partners.html"
