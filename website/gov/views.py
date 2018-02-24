from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class IndexView(generic.ListView):
    template_name = 'gov/index.html'

    def get_queryset(self):
        return Album.objects.all()
    