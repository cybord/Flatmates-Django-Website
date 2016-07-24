from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.template import loader

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

app_name='flatmates'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login1, name='login'),
    url(r'^logout/$', views.logout1, name='logout'),
]