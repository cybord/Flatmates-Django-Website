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
from .forms.user import RegisterForm, ExpenseForm, ChangePasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from .models import userProfile, Expenses
from .utils import calculate
from django.contrib.auth import views
from django.contrib import messages

from django import forms
import django_excel as excel



def home(request):
    if request.user.is_authenticated():

        today = datetime.date.today()
        total,  list = calculate()
        last_5_expenses = Expenses.objects.filter(spent_date__year=today.year, spent_date__month=today.month).order_by('-spent_date')[:5]
        return render(request, 'flatmates/welcome.html', {
            'user': User.objects.get(username=request.user.username).userprofile.full_name,
            'expenses': last_5_expenses,
            'total': total,
            'list': list, } )
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

class Login(generic.View):
    template_name = 'flatmates/login.html'

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('flatmates:home'))

        else:
            if 'next' in request.GET:
                redirect_to = request.GET['next']
                return render(request, self.template_name, {'next': redirect_to} )
            else: return render(request, self.template_name, )


    def post(self,request):
        redirect_to = request.POST['next']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            messages.warning(request, "Please enter correct username and Password")
            return HttpResponseRedirect(reverse('flatmates:login'))

def logout1(request):
    logout(request)
    messages.success(request, "You are logged out successfully.")
    return HttpResponseRedirect(reverse('flatmates:home'))

class Profile(LoginRequiredMixin,generic.View):
    login_url = 'flatmates:login'
    template_name = 'flatmates/profile.html'

    def get(self,request):
        profile = userProfile.objects.get(user_ID=request.user)
        return render(request, self.template_name, {'profile':profile,})


class ChangePassword(LoginRequiredMixin, generic.View):
    login_url = 'flatmates:login'
    template_name = 'flatmates/change_password.html'

    def get(self,request):
        if request.user.is_authenticated():
            form = ChangePasswordForm()
            return render(request, self.template_name, {'form':form,})
        else:
            return HttpResponseRedirect(reverse('flatmates:home'))

    def post(self,request):

        username = request.user.username
        user = User.objects.get(username=request.user.username)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['current_password']):
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    user = authenticate(username=username, password=form.cleaned_data['new_password'])
                    if user is not None:
                        login(request, user)
                        messages.success(self.request, "Your password has been changed successfully.")
                        return HttpResponseRedirect(reverse('flatmates:home'))
                else:
                    form = ChangePasswordForm()
                    return render(request, self.template_name, {'form': form, 'error': "New and Confirm Passwords didn't match"})
            else:
                form = ChangePasswordForm()
                return render(request, self.template_name, {'form': form, 'error': "Please enter correct current Password"})
        else:
            return render(request, self.template_name, {'form': form,})


def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response

class AddExpense(LoginRequiredMixin, generic.View):
    login_url = 'flatmates:login'
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
            if 'submit1' in request.POST:

                return HttpResponseRedirect(reverse('flatmates:home'))
            else:
                form = ExpenseForm()
                return render(request, self.template_name, {'form': form})

        else:
            return render(request, self.template_name, {'form': form})


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


class EditEntries(LoginRequiredMixin, generic.View):
    login_url = 'flatmates:login'
    template_name = 'flatmates/edit_entry.html'

    def get(self,request):
        return render(request, self.template_name,)
