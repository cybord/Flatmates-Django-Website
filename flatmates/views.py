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


#class Home(generic.DetailView):

def home(request):
    if request.user.is_authenticated():
        return render(request, 'flatmates/welcome.html', {
            'user':request.user.username,
            'welcome':'Hi, '})
    else:
        return render(request, 'flatmates/home.html', )


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('flatmates:home'))
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                u = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, u)
                return HttpResponse("Hi, " + u.username)
            else:
                return HttpResponseRedirect(reverse('flatmates:login'))
        else:
            return render(request, 'flatmates/register.html')


def login1(request):
    raise Http404("Poll does not exist")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            greeting = "Hi, " + user.first_name + " " + user.last_name
            return HttpResponse("Hi, " + username)
        else:
            return HttpResponseRedirect(reverse('flatmates:register'))
    else:
        if request.user.is_authenticated():
            return HttpResponse("Hi, " + request.user.username)

        else:
            return render(request, 'flatmates/login.html')


def logout1(request):
    logout(request)
    return HttpResponseRedirect(reverse('flatmates:home'))
