import datetime
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from .forms.user import RegisterForm, ExpenseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import userProfile, Expenses


# class Home(generic.DetailView):

def home(request):
    if request.user.is_authenticated():
        current = (str(timezone.now()))
        date,time = current.split(None,2)
        days = int(date.split("-",3)[2])
        hour,min,sec = (time.split(":",3))
        sec = int(sec.split(".",1)[0])
        month_start_date = timezone.now() - datetime.timedelta(days=days-1,hours=int(hour),minutes=int(min),seconds=int(sec))

        expenses = Expenses.objects.filter(spent_date__gte=month_start_date).order_by('-spent_date')[:5]
        all_expenses = Expenses.objects.filter(spent_date__gte=month_start_date)
        all_users = User.objects.all()

        return render(request, 'flatmates/welcome.html', {
            'user': User.objects.get(username=request.user.username).userprofile.full_name,
            'expenses': expenses,
            'all_expenses': all_expenses,
            'all_users':all_users, 'zone':month_start_date})
    else:
        return render(request, 'flatmates/home.html', )


class Register(generic.View):
    template_name = 'flatmates/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('flatmates:home'))
        else:
            form = RegisterForm()
            return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('flatmates:home'))
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username = form.cleaned_data['username'])
            except User.DoesNotExist:
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                form.cleaned_data['password'])
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                profile = userProfile(user_ID=user, joining_date=form.cleaned_data['joining_date'], company=form.cleaned_data['company'])
                profile.save()
                u = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, u)
                return HttpResponseRedirect(reverse('flatmates:home'))
            else:
                return HttpResponseRedirect(reverse('flatmates:login'))
        else:
            return render(request, self.template_name,{'form':form})



class AddExpense(generic.View):
    template_name = 'flatmates/add_expense.html'

    def get(self,request):
        if request.user.is_authenticated():
            form=ExpenseForm()
            return render(request, self.template_name, {'form': form, })
        else:
            return HttpResponseRedirect(reverse('flatmates:home'))

    def post(self,request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            entry = Expenses.objects.create(id=None, user_name=user, expense=form.cleaned_data['expense'], spent_amount=form.cleaned_data['spent_amount'], description=form.cleaned_data['description'])
            entry.save()
            return HttpResponseRedirect(reverse('flatmates:home'))

        else:
            return render(request, self.template_name, {'form': form})

class Login(generic.View):
    template_name = 'flatmates/login.html'

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('flatmates:home'))

        else:

            return render(request, self.template_name)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('flatmates:home'))
        else:
            return HttpResponseRedirect(reverse('flatmates:login'))

class ViewExpense(LoginRequiredMixin, generic.ListView):
    login_url = 'flatmates:login'
    template_name = 'flatmates/view_expense.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        current = (str(timezone.now()))
        date,time = current.split(None,2)
        days = int(date.split("-",3)[2])
        hour,min,sec = (time.split(":",3))
        sec = int(sec.split(".",1)[0])
        month_start_date = timezone.now() - datetime.timedelta(days=days-1,hours=int(hour),minutes=int(min),seconds=int(sec))

        return Expenses.objects.filter(spent_date__gte=month_start_date).order_by('-spent_date')

def logout1(request):
    logout(request)
    return HttpResponseRedirect(reverse('flatmates:home'))
