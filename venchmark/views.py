# venchmark/views.py
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from assessments.models import Assessment, Framework, FrameworkSource, FrameworkControls, Questionnaire, Report
from companies.models import Company, User
from rest_framework.authtoken.models import Token
#from reports.models import Report
#from frameworks.models import Framework, FrameworkSource, FrameworkControls
#from reports.models import Report
from itertools import chain


class HomePageView(LoginRequiredMixin, TemplateView):
    login_url = '/people/login/'
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_of_companies = Company.objects.all().count()
        context['num_of_companies'] = num_of_companies
        num_of_people = User.objects.all().count()
        context['num_of_people'] = num_of_people
        num_of_assessments = Assessment.objects.all().count()
        context['num_of_assessments'] = num_of_assessments
        num_of_frameworks = Framework.objects.all().count()
        context['num_of_frameworks'] = num_of_frameworks
        num_of_questionnaires = Questionnaire.objects.all().count()
        context['num_of_questionnaires'] = num_of_questionnaires
        num_of_reports = Report.objects.all().count()
        context['num_of_reports'] = num_of_reports
        token = Token.objects.get(user=self.request.user)
        context['token'] = token
        return context

def redirect_home_view(request):
    response = redirect('login')
    return response

class PasswordResetPageView(TemplateView):
    template_name = 'password.html'

def logout_view(request):
    response = redirect('login')
    return response
