from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView


# Create your views here.

class Index(TemplateView):
    template_name = "body.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['title_body'] = 'Secretaria de Portuguesa'
        return context
